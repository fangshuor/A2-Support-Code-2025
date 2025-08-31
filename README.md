# Assignment 2 Support Code

This is the support code for COMP3702 Assignment 2 "Cheese Hunter", 2025.

The following files are provided:

**game_env.py**

This file contains a class representing a Cheese Hunter level environment, storing the dimensions of the environment, initial player position, exit (cheese) position, lever positions, trap positions, mapping of levers to traps, targets for path cost, run time and number of nodes expanded, the tile type of each grid position, and a list of all available actions.

This file contains a number of functions which will be useful in developing your solver:

~~~~~
__init__(filename)
~~~~~
Constructs a new instance based on the given input filename.


~~~~~
get_init_state()
~~~~~
Returns a GameState object (see below) representing the initial state of the level.


~~~~~
perform_action(state, action)
~~~~~
Simulates the outcome of performing the given 'action' starting from the given 'state', where 'action' is an element of GameEnv.ACTIONS and 'state' is a GameState object. Returns a tuple (valid, reward, next_state, terminal), where success is True (if the action can be performed) or False (if the action is cannot be performed), reward is a float of the reward received from performing the action from the state, next_state is a GameState
object of the next state the player ends up in, and terminal is True (if the state is solved or game over) or False (if the state is not solved or game over).


~~~~~
is_solved(state)
~~~~~
Checks whether the given 'state' (a GameState object) is solved (i.e. player at exit). Returns True (solved) or False (not solved).


~~~~~
is_game_over(state)
~~~~~
Checks whether the given 'state' (a GameState object) results in game over (i.e. the player is standing on a cheese trap). Returns True (game over) or False (not game over).


~~~~~
render(state)
~~~~~
Prints a graphical representation of the given 'state' (a GameState object) to the terminal - you may find this useful for debugging.


**game_state.py**

This file contains a class representing a Cheese Hunter state, storing the position of the player and the status of all levers/traps in the level (1 for activated, 0 for unactivated).

~~~~~
__init__(row, col)
~~~~~
Constructs a new GameState instance, where row and column are integers between 0 and n_rows, n_cols respectively.


**play_game.py**

This file contains a script which launches an interactive game session when run. Becoming familiar with the game mechanics may be helpful in designing your solution.

To start playing, try:
`python play_game.py testcases/level_1.txt`

The script takes 1 command line argument:
- input_filename, which must be a valid testcase file (e.g. one of the provided files in the testcases directory)

When prompted for an action, type one of the available action strings (e.g. wr, wl, etc) and press enter to perform the entered action (make sure the terminal and not the display window is selected when entering actions).


**solution.py**

Template file for you to implement your solution to Assignment 2.

You should implement each of the method stubs contained in this file. You may add additional methods and/or classes to this file if you wish. You may also create additional source files and import to this file if you wish.

We recommend you implement Value Iteration first, then attempt Policy Iteration after your Value Iteration implementation is working.


**tester.py**

This file contains a script which can be used to debug and/or evaluate your solution.

The script takes up to 3 command line arguments:
- search_type, which should be "vi" or "pi"
- testcase_filename, which must be a valid testcase file (e.g. one of the provided files in the testcases directory)
- (optional) "-v" to enable visualisation of the resulting trajectory


**testcases**

A directory containing input files which can be used to evaluate your solution.

The format of a testcase file is:
~~~~~
n_rows, n_cols
gamma, epsilon
VI time targets (min score target, max score target)
PI time targets (min score target, max score target)
VI iterations targets (min score target, max score target)
PI iterations targets (min score target, max score target)
reward target
trapdoor probability
jump probability
walking probabilities
ladder fall probability
collision penalty
game over penalty
episode seed
grid data

grid_data (row 1)
...
grid_data (row n_rows)
~~~~~

Testcase files can contain comments, starting with '#', which are ignored by the input file parser.
