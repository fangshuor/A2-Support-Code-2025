from game_env import GameEnv
from game_state import GameState
import numpy as np
import random
from collections import deque

"""
solution.py

This file is a template you should use to implement your solution.

You should implement each of the method stubs below. You may add additional methods and/or classes to this file if you
wish. You may also create additional source files and import to this file if you wish.

COMP3702 Assignment 2 "Cheese Hunter" Support Code, 2025
"""


class Solver:

    def __init__(self, game_env):
        self.game_env = game_env
        self.ql_iterations = 0
        self.ql_epsilon = None

        # caching for performance
        self.reachable_states = None
        self.valid_actions_cache = {}
        self.transition_cache = {}

        # VI state values
        self.vi_values = {}
        self.vi_prev_values = {}

        # PI policy and values
        self.pi_policy = {}
        self.pi_values = {}

        # Q-learning Q-values
        self.q_values = {}

    @staticmethod
    def get_student_number():
        """Please enter your student number as a return string to this method."""
        return "48885991"

    @staticmethod
    def get_testcases():
        """
        Select which testcases you wish the autograder to test you on.
        The autograder will not run any excluded testcases.
        e.g. [1, 4, 5] will only run testcases 1, 4, and 5, excluding, 2 and 3.
        :return: a list containing which testcase numbers to run (testcases in 1-5).
        """
        return [1, 2, 3, 4, 5]

    @staticmethod
    def get_solution():
        """
        Select which solution you wish the autograder to run, VI (Value Iteration), PI (Policy Iteration),
        and/or QL (Q-Learning). The autograder will only run the specified solution methods.
        :return: a list of strings containing which search methods to run ("value_iteration" to  run VI,
        "policy_iteration" to run PI, and "q-learning" to run QL).
        """
        return ["value_iteration", "policy_iteration", "q-learning"]

    # === Value Iteration ==============================================================================================

    def vi_initialise(self):
        """
        Initialise any variables required before the start of Value Iteration.
        """
        self.reachable_states = self.build_reachable_states()
        self.vi_values = {s: 0.0 for s in self.reachable_states}
        self.vi_prev_values = {s: 0.0 for s in self.reachable_states}

    def vi_is_converged(self):
        """
        Check if Value Iteration has reached convergence.
        :return: True if converged, False otherwise
        """
        max_diff = 0.0
        for state in self.reachable_states:
            diff = abs(self.vi_values[state] - self.vi_prev_values[state])
            if diff > max_diff:
                max_diff = diff
        return max_diff < self.game_env.epsilon

    def vi_iteration(self):
        """
        Perform a single iteration of Value Iteration (i.e. loop over the state space once).
        """
        for k in self.vi_values:
            self.vi_prev_values[k] = self.vi_values[k]

        for state in self.reachable_states:
            if self.game_env.is_solved(state) or self.game_env.is_game_over(state):
                self.vi_values[state] = 0.0
                continue

            max_q = float('-inf')
            for action in self.get_valid_actions(state):
                q_val = 0.0
                for prob, reward, next_state in self.get_transition_outcomes(state, action):
                    next_val = self.vi_values.get(next_state, 0.0)
                    q_val += prob * (reward + self.game_env.gamma * next_val)
                if q_val > max_q:
                    max_q = q_val

            self.vi_values[state] = max_q if max_q > float('-inf') else 0.0

    def vi_plan_offline(self):
        """
        Plan using Value Iteration.
        """
        # !!! In order to ensure compatibility with tester, you should not modify this method !!!
        self.vi_initialise()
        while True:
            self.vi_iteration()

            # NOTE: vi_iteration is always called before vi_is_converged
            if self.vi_is_converged():
                break

    def vi_get_state_value(self, state: GameState):
        """
        Retrieve V(s) for the given state.
        :param state: the current state
        :return: V(s)
        """
        return self.vi_values.get(state, 0.0)

    def vi_select_action(self, state: GameState):
        """
        Retrieve the optimal action for the given state (based on values computed by Value Iteration).
        :param state: the current state
        :return: optimal action for the given state (element of GameEnv.ACTIONS)
        """
        best_action = None
        best_q = float('-inf')

        for action in self.get_valid_actions(state):
            q_val = 0.0
            for prob, reward, next_state in self.get_transition_outcomes(state, action):
                next_val = self.vi_values.get(next_state, 0.0)
                q_val += prob * (reward + self.game_env.gamma * next_val)
            if q_val > best_q:
                best_q = q_val
                best_action = action

        return best_action

    # === Policy Iteration =============================================================================================

    def pi_initialise(self):
        """
        Initialise any variables required before the start of Policy Iteration.
        """
        if self.reachable_states is None:
            self.reachable_states = self.build_reachable_states()

        self.pi_values = {s: 0.0 for s in self.reachable_states}
        self.pi_policy = {}
        for state in self.reachable_states:
            valid = self.get_valid_actions(state)
            if valid:
                self.pi_policy[state] = valid[0]

        self.pi_prev_policy = {}

    def pi_is_converged(self):
        """
        Check if Policy Iteration has reached convergence.
        :return: True if converged, False otherwise
        """
        return self.pi_policy == self.pi_prev_policy

    def pi_iteration(self):
        """
        Perform a single iteration of Policy Iteration (i.e. perform one step of policy evaluation and one step of
        policy improvement).
        """
        self.pi_prev_policy = self.pi_policy.copy()

        n = len(self.reachable_states)
        state_idx = {s: i for i, s in enumerate(self.reachable_states)}

        A = np.zeros((n, n))
        b = np.zeros(n)

        for state in self.reachable_states:
            if self.game_env.is_solved(state) or self.game_env.is_game_over(state):
                continue

            i = state_idx[state]
            action = self.pi_policy.get(state)
            if action is None:
                continue

            A[i, i] = 1.0
            for prob, reward, next_state in self.get_transition_outcomes(state, action):
                b[i] += prob * reward
                if next_state in state_idx:
                    j = state_idx[next_state]
                    A[i, j] -= self.game_env.gamma * prob

        for state in self.reachable_states:
            if self.game_env.is_solved(state) or self.game_env.is_game_over(state):
                i = state_idx[state]
                A[i, i] = 1.0
                b[i] = 0.0

        values = np.linalg.solve(A, b)
        for state in self.reachable_states:
            self.pi_values[state] = values[state_idx[state]]

        for state in self.reachable_states:
            if self.game_env.is_solved(state) or self.game_env.is_game_over(state):
                continue

            best_action = None
            best_q = float('-inf')
            for action in self.get_valid_actions(state):
                q_val = 0.0
                for prob, reward, next_state in self.get_transition_outcomes(state, action):
                    next_val = self.pi_values.get(next_state, 0.0)
                    q_val += prob * (reward + self.game_env.gamma * next_val)
                if q_val > best_q:
                    best_q = q_val
                    best_action = action

            if best_action is not None:
                self.pi_policy[state] = best_action

    def pi_plan_offline(self):
        """
        Plan using Policy Iteration.
        """
        # !!! In order to ensure compatibility with tester, you should not modify this method !!!
        self.pi_initialise()
        while True:
            self.pi_iteration()

            # NOTE: pi_iteration is always called before pi_is_converged
            if self.pi_is_converged():
                break

    def pi_select_action(self, state: GameState):
        """
        Retrieve the optimal action for the given state (based on values computed by Policy Iteration).
        :param state: the current state
        :return: optimal action for the given state (element of GameEnv.ACTIONS)
        """
        return self.pi_policy.get(state)

    # === Q-Learning =============================================================================================

    def ql_initialise(self):
        """
        Initialise any variables required before the start of Q-Learning.
        """
        self.q_values = {}
        self.ql_epsilon = self.game_env.ql_epsilon_start

        self.ql_valid_actions = {}

    def ql_iteration(self):
        """
        Perform a single iteration of Q-Learning (i.e. begin from init_state and run one episode, i.e. till the agent
        reaches a terminal state).
        """
        self.ql_iterations += 1

        state = self.game_env.get_init_state()

        while not (self.game_env.is_solved(state) or self.game_env.is_game_over(state)):
            if random.random() < self.ql_epsilon:
                if state in self.ql_valid_actions:
                    valid_actions = self.ql_valid_actions[state]
                else:
                    valid_actions = []
                    for a in self.game_env.ACTIONS:
                        if self.game_env.perform_action(state, a, seed=0)[0]:
                            valid_actions.append(a)
                    self.ql_valid_actions[state] = valid_actions

                if not valid_actions:
                    break
                action = random.choice(valid_actions)
            else:
                if state in self.ql_valid_actions:
                    valid_actions = self.ql_valid_actions[state]
                else:
                    valid_actions = []
                    for a in self.game_env.ACTIONS:
                        if self.game_env.perform_action(state, a, seed=0)[0]:
                            valid_actions.append(a)
                    self.ql_valid_actions[state] = valid_actions

                if not valid_actions:
                    break

                best_action = None
                best_q = float('-inf')
                for a in valid_actions:
                    q = self.q_values.get((state, a), 0.0)
                    if q > best_q:
                        best_q = q
                        best_action = a
                action = best_action

            is_valid, reward, next_state, is_terminal = self.game_env.perform_action(state, action)

            if not is_valid:
                break

            max_next_q = 0.0
            if not is_terminal:
                for a in self.game_env.ACTIONS:
                    q = self.q_values.get((next_state, a), 0.0)
                    if q > max_next_q:
                        max_next_q = q

            current_q = self.q_values.get((state, action), 0.0)
            self.q_values[(state, action)] = current_q + self.game_env.learning_rate * (
                reward + self.game_env.gamma * max_next_q - current_q
            )

            state = next_state

        self.ql_epsilon_decay()

    def ql_epsilon_decay(self):
        """
        Decay the epsilon-greedy value for Q-Learning to choose between exploration vs exploitation.
        """
        self.ql_epsilon = max(
            self.game_env.ql_epsilon_end,
            self.game_env.ql_epsilon_start
            * (self.game_env.ql_epsilon_decay**self.ql_iterations),
        )

    def ql_plan_offline(self):
        """
        Plan using Q-Learning.
        """
        # !!! In order to ensure compatibility with tester, you should not modify this method !!!
        self.ql_initialise()
        while True:
            self.ql_iteration()

    def ql_select_action(self, state: GameState):
        """
        Retrieve the optimal action for the given state (based on values computed by Q-Learning).
        :param state: the current state
        :return: optimal action for the given state (element of GameEnv.ACTIONS)
        """
        best_action = None
        best_q = float('-inf')

        for action in self.get_valid_actions(state):
            q = self.q_values.get((state, action), 0.0)
            if q > best_q:
                best_q = q
                best_action = action

        return best_action

    def ql_get_state_action_value(self, state: GameState, action: str):
        """
        Retrieve the Q-value for a given state-action pair.
        :param state: the current state
        :param action: the current action
        """
        return self.q_values.get((state, action), 0.0)

    # === Helper Methods ===============================================================================================

    def build_reachable_states(self):
        # BFS to find all reachable states from initial position
        visited = set()
        queue = deque([self.game_env.get_init_state()])
        visited.add(self.game_env.get_init_state())

        while queue:
            state = queue.popleft()
            if self.game_env.is_solved(state) or self.game_env.is_game_over(state):
                continue

            for action in self.game_env.ACTIONS:
                for _, _, next_state in self.get_transition_outcomes(state, action):
                    if next_state not in visited:
                        visited.add(next_state)
                        queue.append(next_state)

        return list(visited)

    def get_valid_actions(self, state):
        if state in self.valid_actions_cache:
            return self.valid_actions_cache[state]

        valid = []
        for action in self.game_env.ACTIONS:
            is_valid, _, _, _ = self.game_env.perform_action(state, action, seed=0)
            if is_valid:
                valid.append(action)

        self.valid_actions_cache[state] = valid
        return valid

    def get_transition_outcomes(self, state, action):
        # return list of (probability, reward, next_state) tuples
        cache_key = (state, action)
        if cache_key in self.transition_cache:
            return self.transition_cache[cache_key]

        outcomes = []
        is_valid = self.game_env.perform_action(state, action, seed=0)[0]
        if not is_valid:
            self.transition_cache[cache_key] = outcomes
            return outcomes

        standing_tile = self.game_env.grid_data[state.row + 1][state.col]

        if action in {self.game_env.WALK_LEFT, self.game_env.WALK_RIGHT}:
            direction = (0, -1) if action == self.game_env.WALK_LEFT else (0, 1)

            if standing_tile == self.game_env.TRAPDOOR:
                for dist in range(3):
                    next_s, rew = self._apply_walk(state, direction, dist)
                    prob = self.game_env.walking_probs[dist]
                    outcomes.append((prob * (1 - self.game_env.trapdoor_prob), rew, next_s))

                next_s_fall, rew_fall = self._apply_fall(state, (1, 0), 1, True)
                outcomes.append((self.game_env.trapdoor_prob, rew_fall, next_s_fall))

            elif standing_tile == self.game_env.LADDER_TILE:
                for dist in range(3):
                    next_s, rew = self._apply_walk(state, direction, dist)
                    prob = self.game_env.walking_probs[dist]
                    outcomes.append((prob * (1 - self.game_env.ladder_fall_prob), rew, next_s))

                next_s_fall, rew_fall = self._apply_fall(state, (1, 0), 2, False)
                outcomes.append((self.game_env.ladder_fall_prob, rew_fall, next_s_fall))

            else:
                for dist in range(3):
                    next_s, rew = self._apply_walk(state, direction, dist)
                    prob = self.game_env.walking_probs[dist]
                    outcomes.append((prob, rew, next_s))

        elif action == self.game_env.JUMP:
            if standing_tile == self.game_env.TRAPDOOR:
                next_s_fall, rew_fall = self._apply_fall(state, (1, 0), 1, True)
                outcomes.append((self.game_env.trapdoor_prob, rew_fall, next_s_fall))

                for dist in [1, 2]:
                    prob_jump = self.game_env.jump_prob if dist == 2 else (1 - self.game_env.jump_prob)
                    next_s, rew = self._apply_movement(state, (-1, 0), dist, False)
                    outcomes.append((prob_jump * (1 - self.game_env.trapdoor_prob), rew, next_s))
            else:
                for dist in [1, 2]:
                    prob = self.game_env.jump_prob if dist == 2 else (1 - self.game_env.jump_prob)
                    next_s, rew = self._apply_movement(state, (-1, 0), dist, False)
                    outcomes.append((prob, rew, next_s))

        elif action == self.game_env.CLIMB:
            next_s_up, rew_up = self._apply_movement(state, (-1, 0), 1, False)
            outcomes.append((1 - self.game_env.ladder_fall_prob, rew_up, next_s_up))

            next_s_fall, rew_fall = self._apply_fall(state, (1, 0), 2, False)
            outcomes.append((self.game_env.ladder_fall_prob, rew_fall, next_s_fall))

        elif action == self.game_env.DROP:
            if self.game_env.grid_data[state.row][state.col] == self.game_env.LADDER_TILE:
                next_s_down, rew_down = self._apply_movement(state, (1, 0), 1, False)
                outcomes.append((1 - self.game_env.ladder_fall_prob, rew_down, next_s_down))

                next_s_fall, rew_fall = self._apply_fall(state, (1, 0), 2, False)
                outcomes.append((self.game_env.ladder_fall_prob, rew_fall, next_s_fall))
            else:
                next_s, rew = self._apply_movement(state, (1, 0), 1, False)
                outcomes.append((1.0, rew, next_s))

        self.transition_cache[cache_key] = outcomes
        return outcomes

    def _apply_walk(self, state, direction, dist):
        reward = -self.game_env.ACTION_COST[self.game_env.WALK_LEFT]
        next_state = state

        for step in range(1, dist + 1):
            check_col = state.col + step * direction[1]
            if not (0 <= check_col < self.game_env.n_cols):
                reward -= self.game_env.collision_penalty
                break
            if self.game_env.grid_data[state.row][check_col] in {self.game_env.SOLID_TILE, self.game_env.TRAPDOOR}:
                reward -= self.game_env.collision_penalty
                break
            next_state = GameState(state.row, check_col)
            if self.game_env.is_game_over(next_state):
                reward -= self.game_env.game_over_penalty
                break

        return next_state, reward

    def _apply_movement(self, state, direction, dist, trapdoor_open):
        action_type = self.game_env.JUMP if direction[0] == -1 else (self.game_env.CLIMB if direction == (-1, 0) else self.game_env.DROP)
        reward = -self.game_env.ACTION_COST[action_type]
        next_state = state

        for step in range(1, dist + 1):
            check_row = state.row + step * direction[0]
            check_col = state.col + step * direction[1]

            if not (0 <= check_row < self.game_env.n_rows):
                reward -= self.game_env.collision_penalty
                break
            if not (0 <= check_col < self.game_env.n_cols):
                reward -= self.game_env.collision_penalty
                break

            if direction[0] != 0:
                if self.game_env.grid_data[check_row][state.col] == self.game_env.SOLID_TILE:
                    reward -= self.game_env.collision_penalty
                    break
                if self.game_env.grid_data[check_row][state.col] == self.game_env.TRAPDOOR and not trapdoor_open:
                    reward -= self.game_env.collision_penalty
                    break
                next_state = GameState(check_row, state.col)
            else:
                if self.game_env.grid_data[state.row][check_col] in {self.game_env.SOLID_TILE, self.game_env.TRAPDOOR}:
                    reward -= self.game_env.collision_penalty
                    break
                next_state = GameState(state.row, check_col)

            if self.game_env.is_game_over(next_state):
                reward -= self.game_env.game_over_penalty
                break

        return next_state, reward

    def _apply_fall(self, state, direction, max_dist, trapdoor_open):
        action_type = self.game_env.DROP
        reward = -self.game_env.ACTION_COST[action_type]
        next_state = state

        actual_dist = 0
        for step in range(1, max_dist + 1):
            check_row = state.row + step * direction[0]

            if not (0 <= check_row < self.game_env.n_rows):
                if actual_dist == 0:
                    reward -= self.game_env.collision_penalty
                break

            tile = self.game_env.grid_data[check_row][state.col]
            if tile == self.game_env.SOLID_TILE or (tile == self.game_env.TRAPDOOR and not trapdoor_open):
                if actual_dist == 0:
                    reward -= self.game_env.collision_penalty
                break

            next_state = GameState(check_row, state.col)
            actual_dist += 1

            if self.game_env.is_game_over(next_state):
                reward -= self.game_env.game_over_penalty
                break

        return next_state, reward


