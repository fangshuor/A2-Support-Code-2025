"""
game_state.py

This file contains a class representing a Cheese Hunter state. You should make use of this class in your solver.

COMP3702 Assignment 2 "Cheese Hunter" Support Code, 2025
"""


class GameState:
    """
    Instance of a Cheese Hunter state. row and col represent the current player position.

    You may use this class and its functions, but should avoid modifying it to ensure compatibility with the Tester.
    """

    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __eq__(self, other):
        if not isinstance(other, GameState):
            return False
        return self.row == other.row and self.col == other.col

    def __hash__(self):
        return hash((self.row, self.col))

    def __repr__(self):
        return f'row: {self.row},\t\t col: {self.col}'

    def deepcopy(self):
        return GameState(self.row, self.col)
