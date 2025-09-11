from game_env import GameEnv
from game_state import GameState

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

        #
        #
        # TODO: Define any class instance variables you require here (avoid performing any computationally expensive
        #  heuristic preprocessing operations here - use the preprocess_heuristic method below for this purpose).
        #
        #

    @staticmethod
    def get_student_number():
        """Please enter your student number as a return string to this method."""
        return "0"

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
        #
        # TODO: Implement any initialisation for Value Iteration (e.g. building a list of states) here. You should not
        #  perform value iteration in this method.
        #
        # In order to ensure compatibility with tester, you should avoid adding additional arguments to this function.
        #
        pass

    def vi_is_converged(self):
        """
        Check if Value Iteration has reached convergence.
        :return: True if converged, False otherwise
        """
        #
        # TODO: Implement code to check if Value Iteration has reached convergence here.
        #
        # In order to ensure compatibility with tester, you should avoid adding additional arguments to this function.
        #
        pass

    def vi_iteration(self):
        """
        Perform a single iteration of Value Iteration (i.e. loop over the state space once).
        """
        #
        # TODO: Implement code to perform a single iteration of Value Iteration here.
        #
        # In order to ensure compatibility with tester, you should avoid adding additional arguments to this function.
        #
        pass

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
        #
        # TODO: Implement code to return the value V(s) for the given state (based on your stored VI values) here. If a
        #  value for V(s) has not yet been computed, this function should return 0.
        #
        # In order to ensure compatibility with tester, you should avoid adding additional arguments to this function.
        #
        pass

    def vi_select_action(self, state: GameState):
        """
        Retrieve the optimal action for the given state (based on values computed by Value Iteration).
        :param state: the current state
        :return: optimal action for the given state (element of GameEnv.ACTIONS)
        """
        #
        # TODO: Implement code to return the optimal action for the given state (based on your stored VI values) here.
        #
        # In order to ensure compatibility with tester, you should avoid adding additional arguments to this function.
        #
        pass

    # === Policy Iteration =============================================================================================

    def pi_initialise(self):
        """
        Initialise any variables required before the start of Policy Iteration.
        """
        #
        # TODO: Implement any initialisation for Policy Iteration (e.g. building a list of states) here. You should not
        #  perform policy iteration in this method.
        #
        # In order to ensure compatibility with tester, you should avoid adding additional arguments to this function.
        #
        pass

    def pi_is_converged(self):
        """
        Check if Policy Iteration has reached convergence.
        :return: True if converged, False otherwise
        """
        #
        # TODO: Implement code to check if Policy Iteration has reached convergence here.
        #
        # In order to ensure compatibility with tester, you should avoid adding additional arguments to this function.
        #
        pass

    def pi_iteration(self):
        """
        Perform a single iteration of Policy Iteration (i.e. perform one step of policy evaluation and one step of
        policy improvement).
        """
        #
        # TODO: Implement code to perform a single iteration of Policy Iteration (evaluation + improvement) here.
        #
        # In order to ensure compatibility with tester, you should avoid adding additional arguments to this function.
        #
        pass

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
        #
        # TODO: Implement code to return the optimal action for the given state (based on your stored PI policy) here.
        #
        # In order to ensure compatibility with tester, you should avoid adding additional arguments to this function.
        #
        pass

    # === Q-Learning =============================================================================================

    def ql_initialise(self):
        """
        Initialise any variables required before the start of Q-Learning.
        """
        #
        # TODO: Implement any initialisation for Q-Learning (e.g. building a list of states) here. You should not
        #         #  perform q-learning in this method.
        #
        # In order to ensure compatibility with tester, you should avoid adding additional arguments to this function.
        #
        pass

    def ql_iteration(self):
        """
        Perform a single iteration of Policy Iteration (i.e. perform one step of policy evaluation and one step of
        policy improvement).
        """
        #
        # TODO: Implement code to perform a single iteration of Q-Learning here.
        #
        # In order to ensure compatibility with tester, you should avoid adding additional arguments to this function.
        # You should also perform "self.ql_iterations += 1" at the start of an iteration and "self.ql_epsilon_decay()"
        # at the end of an iteration.
        #
        self.ql_iterations += 1
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
        #
        # TODO: Implement code to return the optimal action for the given state (based on your stored QL policy) here.
        #
        # In order to ensure compatibility with tester, you should avoid adding additional arguments to this function.
        #
        pass

    def ql_get_state_action_value(self, state: GameState, action: str):
        """
        Retrieve the Q-value for a given state-action pair.
        :param state: the current state
        :param action: the current action
        """
        #
        # TODO: Implement code to return the Q-value for a given state-action pair (based on the learned Q-values) here.
        #
        # In order to ensure compatibility with tester, you should avoid adding additional arguments to this function.
        #
        pass

    # === Helper Methods ===============================================================================================
    #
    #
    # TODO: Add any additional methods here
    #
    #


