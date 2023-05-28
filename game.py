import pygame

from const import *

from board import Board
from render import Render


class Game:
    """
    Class Game
    """

    def __init__(self, AI=0):
        """
        Constructor
        """
        self.board = Board()
        self.render = Render()
        self.player = PLAYER_X
        self.playing = True
        self.player_playing = True
        self.AI = AI
        pygame.font.init()

        if AI == 1:
            pass
        elif AI == 2:
            self.player_playing = False

    def render_screen_game(self, surface):
        """
        render the board
        :param surface: current surface
        :return:
        """
        self.render.create_board(surface, self.board)
        self.render.draw_status(surface, self.board, self.player, abs(self.board.value))
        self.draw_player(surface)
        self.render.draw(surface, self.board)
        self.draw_board_valid(surface, self.playing)

    def next_turn(self):
        """
        get the next turn
        :return:
        """
        self.player = PLAYER_X if self.player == PLAYER_O else PLAYER_O

    def draw_board_valid(self, surface, is_draw):
        if not is_draw:
            return

        sqr = self.board.squares[self.board.valid_row][self.board.valid_col]
        if sqr.value == 2:
            self.render.draw_board_valid(surface, sqr)

    def draw_player(self, surface):
        if self.AI == 0:
            self.render.draw_player(surface, self.board, self.player, "Player 1")
            self.render.draw_player(surface, self.board, -self.player, "Player 2")
        elif self.AI == 1:
            self.render.draw_player(surface, self.board, self.player, "Player 1")
            self.render.draw_player(surface, self.board, -self.player, "AI")
        elif self.AI == 2:
            self.render.draw_player(surface, self.board, self.player, "AI 1")
            self.render.draw_player(surface, self.board, -self.player, "AI 2")

    def play_turn(self, col, row):
        """
        Play a turn
        :param col: current column
        :param row: current row
        :return:
        """
        if self.board.valid_sqr(col, row):
            self.board.mark_sqr(col, row, self.player)
            self.check_winner(col, row)
            if not self.playing:
                return

            self.next_turn()
            self.board.valid_col = col % 3
            self.board.valid_row = row % 3

    def play_turn_click(self, xclick, yclick):
        """
        Play a turn click on the screen
        :param xclick: current coordinates X
        :param yclick: current coordinates Y
        :return:
        """
        col, row = self.render.convert_coord_of_screen_to_board(xclick, yclick, self.board)
        self.play_turn(col, row)

    def check_winner(self, col, row):
        """
        Check win
        :return:
        """
        main_row = row // 3
        main_col = col // 3
        sqr = self.board.squares[main_row][main_col]

        matrix = []
        for r in range(DIM):
            m = []
            for c in range(DIM):
                m.append(sqr.squares[r][c])
            matrix.append(m)

        is_check_winner = self.board.check_win(matrix)
        if not is_check_winner == 2:
            self.board.squares[main_row][main_col].value = is_check_winner

        matrix = []
        for r in range(DIM):
            m = []
            for c in range(DIM):
                m.append(self.board.squares[r][c].value)
            matrix.append(m)

        is_check_winner = self.board.check_win(matrix)
        if not is_check_winner == 2:
            self.board.value = is_check_winner
            self.playing = False

    def restart(self):
        """
        Reset the board
        :return:
        """
        self.__init__()
