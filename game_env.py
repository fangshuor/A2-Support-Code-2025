import random

from game_state import GameState

"""
game_env.py

This file contains a class representing a Cheese Hunter environment. You should make use of this class in your
solver.

COMP3702 Assignment 2 "Cheese Hunter" Support Code, 2025
"""


class GameEnv:
    """
    Instance of a Cheese Hunter environment. Stores the dimensions of the environment, initial player position,
    goal position, lever positions, trap positions, mapping of levers to traps, time limit, cost target,
    the tile type of each grid position, and a list of all available actions.

    The grid is indexed top to bottom, left to right (i.e. the top left corner has coordinates (0, 0) and the bottom
    right corner has coordinates (n_rows-1, n_cols-1)).

    You may use and modify this class however you want. Note that evaluation on GradeScope will use an unmodified
    GameEnv instance as a simulator.
    """

    # Input file symbols
    SOLID_TILE = "X"
    LADDER_TILE = "="
    AIR_TILE = " "
    TRAPDOOR = "T"
    GOAL_TILE = "G"
    PLAYER_TILE = "P"
    CHEESE_TRAP = "C"
    VALID_TILES = {
        SOLID_TILE,
        LADDER_TILE,
        AIR_TILE,
        TRAPDOOR,
        GOAL_TILE,
        PLAYER_TILE,
    }

    # Action symbols (i.e. output file symbols)
    WALK_LEFT = "wl"
    WALK_RIGHT = "wr"
    JUMP = "j"
    CLIMB = "c"
    DROP = "d"
    ACTIONS = {
        WALK_LEFT,
        WALK_RIGHT,
        CLIMB,
        DROP,
        JUMP,
    }
    ACTION_COST = {
        WALK_LEFT: 1.0,
        WALK_RIGHT: 1.0,
        CLIMB: 2.0,
        DROP: 0.5,
        JUMP: 2.0,
    }

    def __init__(self, filename):
        """
        Process the given input file and create a new game environment instance based on the input file.
        :param filename: name of input file
        """
        with open(filename, "r") as f:
            # read testcase parameters
            try:
                self.n_rows, self.n_cols = tuple(
                    [int(x) for x in get_line(f).split(",")]
                )
            except ValueError:
                assert False, "/!\\ ERROR: Invalid input file - n_rows and n_cols"
            try:
                self.gamma, self.epsilon = tuple(
                    [float(x) for x in get_line(f).split(",")]
                )
            except ValueError:
                assert False, "/!\\ ERROR: Invalid input file - gamma and epsilon"
            try:
                self.ql_epsilon_start, self.ql_epsilon_end, self.ql_epsilon_decay, self.learning_rate = tuple(
                    [float(x) for x in get_line(f).split(",")]
                )
            except ValueError:
                assert False, "/!\\ ERROR: Invalid input file - QL epsilon start, end, decay, and learning rate"
            try:
                self.vi_time_min_tgt, self.vi_time_max_tgt = tuple(
                    [float(x) for x in get_line(f).split(",")]
                )
            except ValueError:
                assert False, "/!\\ ERROR: Invalid input file - VI time targets"
            try:
                self.pi_time_min_tgt, self.pi_time_max_tgt = tuple(
                    [float(x) for x in get_line(f).split(",")]
                )
            except ValueError:
                assert False, "/!\\ ERROR: Invalid input file - PI time targets"
            try:
                self.ql_time_min_tgt, self.ql_time_max_tgt = tuple(
                    [float(x) for x in get_line(f).split(",")]
                )
            except ValueError:
                assert False, "/!\\ ERROR: Invalid input file - QL time targets"
            try:
                self.vi_iter_min_tgt, self.vi_iter_max_tgt = tuple(
                    [int(x) for x in get_line(f).split(",")]
                )
            except ValueError:
                assert False, "/!\\ ERROR: Invalid input file - VI iterations targets"
            try:
                self.pi_iter_min_tgt, self.pi_iter_max_tgt = tuple(
                    [int(x) for x in get_line(f).split(",")]
                )
            except ValueError:
                assert False, "/!\\ ERROR: Invalid input file - PI iterations targets"
            try:
                self.reward_min_tgt, self.reward_max_tgt = tuple(
                    [float(x) for x in get_line(f).split(",")]
                )
            except ValueError:
                assert False, "/!\\ ERROR: Invalid input file - reward targets"
            try:
                self.trapdoor_prob = float(get_line(f))
            except ValueError:
                assert False, "/!\\ ERROR: Invalid input file - trapdoor probability"
            try:
                self.jump_prob = float(get_line(f))
            except ValueError:
                assert False, "/!\\ ERROR: Invalid input file - jump probability"
            try:
                probs = [float(x) for x in get_line(f).split(",")]
                assert sum(probs) == 1, (
                    "/!\\ ERROR: Invalid input file - walking probabilities do not sum to 1"
                )
                self.walking_probs = [probs[0], probs[1], probs[2]]
            except ValueError:
                assert False, "/!\\ ERROR: Invalid input file - walking probabilities"
            try:
                self.ladder_fall_prob = float(get_line(f))
            except ValueError:
                assert False, "/!\\ ERROR: Invalid input file - ladder fall probability"
            try:
                self.collision_penalty = float(get_line(f))
            except ValueError:
                assert False, "/!\\ ERROR: Invalid input file - collision penalty"
            try:
                self.game_over_penalty = float(get_line(f))
            except ValueError:
                assert False, "/!\\ ERROR: Invalid input file - game over penalty"
            try:
                self.episode_seed = int(get_line(f))
            except ValueError:
                assert False, "/!\\ ERROR: Invalid input file - episode seed"

            # read testcase grid data
            grid_data = []
            line = get_line(f)
            i = 0
            while line is not None:
                grid_data.append(list(line))
                assert len(grid_data[-1]) == self.n_cols, (
                    f"/!\\ ERROR: Invalid input file - incorrect map row length (row {i})"
                )
                line = get_line(f)
                i += 1
            assert len(grid_data) == self.n_rows, (
                "/!\\ ERROR: Invalid input file - incorrect number of rows in map"
            )

        # Extract initial, goal, and trap positions
        trap_positions = []  # Record positions of traps
        self.init_row, self.init_col = None, None
        self.goal_row, self.goal_col = None, None
        for r in range(self.n_rows):
            for c in range(self.n_cols):
                if grid_data[r][c] == self.PLAYER_TILE:
                    assert self.init_row is None and self.init_col is None, (
                        "/!\\ ERROR: Invalid input file - more than one initial player position"
                    )
                    self.init_row, self.init_col = r, c
                    # assume player starts on air tile
                    grid_data[r][c] = self.AIR_TILE
                elif grid_data[r][c] == self.GOAL_TILE:
                    assert self.goal_row is None and self.goal_col is None, (
                        "/!\\ ERROR: Invalid input file - more than one exit position"
                    )
                    self.goal_row, self.goal_col = r, c
                    # assume exit is placed on air tile
                    grid_data[r][c] = self.AIR_TILE
                elif grid_data[r][c] == self.TRAPDOOR:
                    trap_positions.append((r, c))

        assert self.init_row is not None and self.init_col is not None, (
            "/!\\ ERROR: Invalid input file - No player initial position"
        )
        assert self.goal_row is not None and self.goal_col is not None, (
            "/!\\ ERROR: Invalid input file - No exit position"
        )

        self.trap_positions = trap_positions
        self.grid_data = grid_data

    def get_init_state(self):
        """
        Get a state representation instance for the initial state.
        :return: initial state
        """
        return GameState(self.init_row, self.init_col)

    def apply_movement(self, state, movement, direction, trapdoor_open):
        """
        Apply movement in specified direction and check if it results in a collision or game over.
        :param state: state to start movement from
        :param movement: movement to apply
        :param direction: direction to apply movement to
        :param trapdoor_open: bool whether a trapdoor has opened beneath player or not
        :return: (collision [True/False], game_over [True/False], next_state [GameState])
        """
        next_state = state.deepcopy()
        for move_row in range(1, movement[0] + 1):
            check_row = state.row + (move_row * direction[0])
            if self.grid_data[check_row][state.col] == self.SOLID_TILE or (
                not 0 <= check_row < self.n_rows
            ):
                return True, False, next_state
            elif (
                self.grid_data[check_row][state.col] == self.TRAPDOOR
                and not trapdoor_open
            ):
                return True, False, next_state
            else:
                next_state = GameState(check_row, state.col)
                if self.is_game_over(next_state):
                    return False, True, next_state

        for move_col in range(1, movement[1] + 1):
            check_col = state.col + (move_col * direction[1])
            if self.grid_data[state.row][check_col] in (
                self.SOLID_TILE,
                self.TRAPDOOR,
            ) or (not 0 <= check_col < self.n_cols):
                return True, False, next_state
            else:
                next_state = GameState(state.row, check_col)
                if self.is_game_over(next_state):
                    return False, True, next_state

        return False, False, next_state

    def perform_action(self, state, action, seed=None):
        """
        Perform the given action on the given state, sample an outcome, and return whether the action was valid, and if
        so, the received reward, the resulting new state and whether the new state is terminal.
        :param state: current GameState
        :param action: an element of self.ACTIONS
        :param seed: random number generator seed (for consistent outcomes between runs)
        :return: (action_is_valid [True/False], received_reward [float], next_state [GameState],
                    state_is_terminal [True/False])
        """
        assert action in self.ACTIONS, (
            "/!\\ ERROR: Invalid action given to perform_action()"
        )
        standing_tile = self.grid_data[state.row + 1][state.col]

        # Check if the action is valid for the given state
        if action in {self.WALK_LEFT, self.WALK_RIGHT, self.JUMP}:
            if standing_tile not in {self.TRAPDOOR, self.SOLID_TILE, self.LADDER_TILE}:
                # Prerequisite not satisfied - can only walk/jump on trapdoors, solids, or ladders
                return False, None, None, None
        elif action == self.CLIMB:
            if self.grid_data[state.row][state.col] != self.LADDER_TILE:
                # Prerequisite not satisfied - must be at ladder to climb
                return False, None, None, None
        else:
            if standing_tile not in {self.AIR_TILE, self.LADDER_TILE, self.TRAPDOOR, self.CHEESE_TRAP}:
                # Prerequisite not satisfied - can only drop through air or ladder tiles
                return False, None, None, None

        random.seed(seed)
        reward = -1 * self.ACTION_COST[action]
        trapdoor_open = False
        movement = (0, 0)
        direction = (0, 0)

        # Handle each action type separately
        if action in {self.WALK_LEFT, self.WALK_RIGHT}:
            # Get direction
            if action == self.WALK_LEFT:
                direction = (0, -1)
            else:
                direction = (0, 1)

            rn = random.random()
            cumulative_prob = 0
            for idx, prob in enumerate(self.walking_probs):
                cumulative_prob += prob
                if rn < cumulative_prob:
                    movement = (0, idx)
                    break

            # Handle differently based on where player is standing
            if standing_tile == self.TRAPDOOR and random.random() < self.trapdoor_prob:
                movement = (1, 0)
                direction = (1, 0)
                trapdoor_open = True
            elif (
                standing_tile == self.LADDER_TILE
                and random.random() < self.ladder_fall_prob
            ):
                movement = (2, 0)
                direction = (1, 0)

        elif action == self.JUMP:
            direction = (-1, 0)
            if random.random() < self.jump_prob:
                movement = (2, 0)
            else:
                movement = (1, 0)

            if standing_tile == self.TRAPDOOR and random.random() < self.trapdoor_prob:
                movement = (1, 0)
                direction = (-1, 0)
                trapdoor_open = True

        elif action == self.CLIMB:
            if random.random() < self.ladder_fall_prob:
                movement = (2, 0)
                direction = (1, 0)
            else:
                movement = (1, 0)
                direction = (-1, 0)

        elif action == self.DROP:
            if self.grid_data[state.row][state.col] == self.LADDER_TILE and random.random() < self.ladder_fall_prob:
                movement = (2, 0)
                direction = (1, 0)
            else:
                movement = (1, 0)
                direction = (1, 0)

        collision, game_over, next_state = self.apply_movement(
            state, movement, direction, trapdoor_open
        )

        if game_over:
            reward -= self.game_over_penalty
        elif collision:
            reward -= self.collision_penalty

        return True, reward, next_state, game_over or self.is_solved(next_state)

    def is_solved(self, state):
        """
        Check if the game has been solved (i.e. player at exit and all levers activated)
        :param state: current GameState
        :return: True if solved, False otherwise
        """
        return state.row == self.goal_row and state.col == self.goal_col

    def is_game_over(self, state):
        """
        Check if a game over situation has occurred (i.e. player has entered on a lava tile)
        :param state: current GameState
        :return: True if game over, False otherwise
        """
        assert 0 < state.row < self.n_rows - 1 and 0 < state.col < self.n_cols - 1, (
            "!!! /!\\ ERROR: Invalid player coordinates !!!"
        )
        return self.grid_data[state.row][state.col] == self.CHEESE_TRAP

    def render(self, state):
        """
        Render the map's current state to terminal
        """
        for r in range(self.n_rows):
            line = ""
            for c in range(self.n_cols):
                if state.row == r and state.col == c:
                    # Current tile is player
                    line += self.grid_data[r][c] + "P" + self.grid_data[r][c]
                elif self.goal_row == r and self.goal_col == c:
                    # Current tile is exit
                    line += self.grid_data[r][c] + "G" + self.grid_data[r][c]
                else:
                    line += self.grid_data[r][c] * 3
            print(line)
        print("\n" * 2)


def get_line(f):
    line = f.readline()
    if len(line) == 0:
        return None
    while line[0] == '#':
        line = f.readline()
    return line.strip()