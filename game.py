from helper import *

from board import Board
from render import Render
from ai import AI


class Game:
    """
    Class Game
    """

    def __init__(self, game_mode=0, level=0, level1=0):
        """
        Constructor
        :param game_mode: current game mode
        - 0: two players
        - 1: one player
        - 2: AI vs AI
        """
        self.board = Board()
        self.render = Render()
        self.player = PLAYER_X
        self.playing = True
        self.player_playing = True
        self.game_mode = game_mode
        self.level = level
        self.level1 = level1
        pygame.font.init()

        if game_mode == 1:
            self.AI = AI(level)
        elif game_mode == 2:
            self.AI = AI(level, 1)
            self.AI1 = AI(level1, -1)
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
        self.render.draw_board(surface, self.board)
        self.draw_board_valid(surface, self.playing)

    def next_turn(self):
        """
        get the next turn
        :return:
        """
        self.player = PLAYER_X if self.player == PLAYER_O else PLAYER_O

    def draw_board_valid(self, surface, is_draw):
        """
        draw the board valid
        :param surface: current surface
        :param is_draw: if true then draw else don't draw
        :return:
        """
        if not is_draw:
            return
        sqr = self.board.squares[self.board.valid_row][self.board.valid_col]
        if sqr.value == 2:
            self.render.draw_board_valid(surface, sqr)

    def draw_player(self, surface):
        """
        draw a text player
        :param surface: current surface
        :return:
        """
        if self.game_mode == 0:
            self.render.draw_player(surface, self.board, PLAYER_X, "Người chơi 1")
            self.render.draw_player(surface, self.board, PLAYER_O, "Người chơi 2")
        elif self.game_mode == 1:
            self.render.draw_player(surface, self.board, PLAYER_X, "Người chơi")
            self.render.draw_player(surface, self.board, PLAYER_O, "AI")
        elif self.game_mode == 2:
            algorithm_AI1 = "minimax" if self.AI.level == 1 else "mtcs"
            algorithm_AI2 = "minimax" if self.AI1.level == 1 else "mtcs"
            self.render.draw_player(surface, self.board, PLAYER_X, f"AI 1-{algorithm_AI1}")
            self.render.draw_player(surface, self.board, PLAYER_O, f"AI 2-{algorithm_AI2}")

    def play_turn(self, col, row):
        """
        Play a turn
        :param col: current column
        :param row: current row
        :return:
        """
        if self.board.valid_sqr(col, row):
            self.board.mark_sqr(col, row, self.player)
            if not self.board.value == 2:
                sound_finish()
                self.playing = False

            self.board.valid_col = col % 3
            self.board.valid_row = row % 3
            if self.playing:
                self.next_turn()

    def play_turn_click(self, xclick, yclick):
        """
        Play a turn click on the screen
        :param xclick: current coordinates X
        :param yclick: current coordinates Y
        :return:
        """
        col, row = self.render.convert_coord_of_screen_to_board(xclick, yclick, self.board)
        self.play_turn(col, row)

    def restart(self):
        """
        Reset the board
        :return:
        """
        self.__init__(self.game_mode, self.level, self.level1)

    def run_ai(self):
        """
        AI play
        :return:
        """
        if not self.playing or self.game_mode == 0:
            return

        if self.game_mode == 1:
            if self.player == self.AI.player:
                self.player_playing = False
                row, col = self.AI.eval(self.board)
                self.play_turn(col, row)
                self.player_playing = True

        elif self.game_mode == 2:
            if self.player == self.AI.player:
                row, col = self.AI.eval(self.board)
                self.play_turn(col, row)
            else:
                row, col = self.AI1.eval(self.board)
                self.play_turn(col, row)



