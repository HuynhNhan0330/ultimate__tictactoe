from const import *


class BoardDim:
    """
    Class BoardDim
    Save property of board
    """

    def __init__(self, size, base_size, xcor, ycor):
        """
        Constructor
        :param size: Size board
        :param base_size: Size base board
        :param xcor: starting X coordinate
        :param ycor: starting Y coordinate
        """
        self.size = size
        self.sqsize = size // DIM  # Size square
        self.base_size = base_size
        self.base_sqsize = base_size // DIM  # Size square
        self.xcor = xcor
        self.ycor = ycor
