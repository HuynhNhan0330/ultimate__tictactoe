from helper import *

from board import Board


class Render:
    """
    Class render
    board to screen
    """

    def __init__(self):
        pass

    def create_board(self, surface, board):
        """
        Render the board (sub)
        :param surface: current surface
        :param board: current board
        :return:
        """
        for row in range(DIM):
            for col in range(DIM):
                sqr = board.squares[row][col]

                if isinstance(sqr, Board):
                    self.create_board(surface, sqr)

        # Point vertical
        pointVerFirstBegin = (board.dims.xcor + board.dims.sqsize, board.dims.ycor)
        pointVerFirstEnd = (board.dims.xcor + board.dims.sqsize, board.dims.ycor + board.dims.size)
        pointVerSecondBegin = (board.dims.xcor + board.dims.size - board.dims.sqsize, board.dims.ycor)
        pointVerSecondEnd = (board.dims.xcor + board.dims.size - board.dims.sqsize, board.dims.ycor + board.dims.size)

        # Point horizontal
        pointHorFirstBegin = (board.dims.xcor, board.dims.ycor + board.dims.sqsize)
        pointHorFirstEnd = (board.dims.xcor + board.dims.size, board.dims.ycor + board.dims.sqsize)
        pointHorSecondBegin = (board.dims.xcor, board.dims.ycor + board.dims.size - board.dims.sqsize)
        pointHorSecondEnd = (board.dims.xcor + board.dims.size, board.dims.ycor + board.dims.size - board.dims.sqsize)

        # Vertical lines
        pygame.draw.line(surface, LINE_COLOR, pointVerFirstBegin, pointVerFirstEnd, board.linewidth)
        pygame.draw.line(surface, LINE_COLOR, pointVerSecondBegin, pointVerSecondEnd, board.linewidth)

        # Horizontal lines
        pygame.draw.line(surface, LINE_COLOR, pointHorFirstBegin, pointHorFirstEnd, board.linewidth)
        pygame.draw.line(surface, LINE_COLOR, pointHorSecondBegin, pointHorSecondEnd, board.linewidth)

    def convert_coord_of_screen_to_board(self, xclick, yclick, board):
        """
        convert screen coordinates to board coordinates
        :param xclick: X coordinate click
        :param yclick: Y coordinate click
        :param board: current board
        :return:
        """
        margin = board.margin

        # Check the position in the board
        if xclick < margin or xclick > margin + SIZE_BOARD or yclick < margin or yclick > margin + SIZE_BOARD:
            return -1, -1

        current_col = (xclick - margin) // SIZE_SQR_SUB_BOARD
        current_row = (yclick - margin) // SIZE_SQR_SUB_BOARD

        return current_col, current_row

    def draw_board(self, surface, board):
        """
        draw board
        :param surface: current surface
        :param board: current board
        :return:
        """
        if board.value == 2 or board.value == 0:
            for rmain in range(DIM):
                for cmain in range(DIM):
                    sqr = board.squares[rmain][cmain]
                    if sqr.value == 2 or sqr.value == 0:
                        for rsub in range(DIM):
                            for csub in range(DIM):
                                sqrsub = sqr.squares[rsub][csub]
                                if not sqr == 2:
                                    self.draw_fig(surface, sqr, csub, rsub)
                    else:
                        self.merge_fig_win(surface, sqr, sqr.value)
        else:
            self.merge_fig_win(surface, board, board.value)

    def draw_fig(self, surface, board, col, row):
        """
        draw fig
        :param surface: current surface
        :param board: current board
        :param col: current column
        :param row: current row
        :return:
        """
        sqr = board.squares[row][col]
        if sqr == PLAYER_X:
            # Desc line
            ipos = (board.dims.xcor + (col * board.dims.sqsize) + board.offset,
                    board.dims.ycor + (row * board.dims.sqsize) + board.offset)
            fpos = (board.dims.xcor + board.dims.sqsize * (1 + col) - board.offset,
                    board.dims.ycor + board.dims.sqsize * (1 + row) - board.offset)
            pygame.draw.line(surface, CROSS_COLOR, ipos, fpos, board.linewidth)

            # Asc line
            ipos = (board.dims.xcor + (col * board.dims.sqsize) + board.offset,
                    board.dims.ycor + board.dims.sqsize * (1 + row) - board.offset)
            fpos = (board.dims.xcor + board.dims.sqsize * (1 + col) - board.offset,
                    board.dims.ycor + (row * board.dims.sqsize) + board.offset)
            pygame.draw.line(surface, CROSS_COLOR, ipos, fpos, board.linewidth)

            # Circle
        elif sqr == PLAYER_O:
            center = (board.dims.xcor + board.dims.sqsize * (0.5 + col),
                      board.dims.ycor + board.dims.sqsize * (0.5 + row))

            pygame.draw.circle(surface, CIRCLE_COLOR, center, board.radius, board.linewidth)

    def merge_fig_win(self, surface, board, winner):
        """
        merge new fig
        :param surface: surface
        :param board: current board
        :param winner: player win
        :return:
        """
        transparent = pygame.Surface((board.dims.size + 5, board.dims.size + 5))
        transparent.fill(FADE)
        surface.blit(transparent, (board.dims.xcor, board.dims.ycor))

        # merge flag
        # cross
        if winner == PLAYER_X:
            # desc line
            ipos = (board.dims.xcor + board.offset,
                    board.dims.ycor + board.offset)
            fpos = (board.dims.xcor + board.dims.size - board.offset,
                    board.dims.ycor + board.dims.size - board.offset)
            pygame.draw.line(surface, CROSS_COLOR, ipos, fpos, board.linewidth + 7)

            # asc line
            ipos = (board.dims.xcor + board.offset,
                    board.dims.ycor + board.dims.size - board.offset)
            fpos = (board.dims.xcor + board.dims.size - board.offset,
                    board.dims.ycor + board.offset)
            pygame.draw.line(surface, CROSS_COLOR, ipos, fpos, board.linewidth + 7)

        # circle
        if winner == PLAYER_O:
            center = (board.dims.xcor + board.dims.size * 0.5,
                      board.dims.ycor + board.dims.size * 0.5)

            pygame.draw.circle(surface, CIRCLE_COLOR, center, board.dims.size * 0.4, board.linewidth + 7)

        board.active = False

    def draw_board_valid(self, surface, board):
        """
        Draw rection valid
        :param surface: current surface
        :param board: current board
        :return:
        """
        xcor = board.dims.xcor
        ycor = board.dims.ycor
        color = BOARD_VALID_COLOR
        pygame.draw.rect(surface, color, (xcor, ycor, board.dims.size, board.dims.size), 3)

    def draw_status(self, surface, board, player, type):
        """
        draw a word when board is finished
        :param surface: current surface
        :param board: current board
        :param win: check win or draw
        :return:
        """
        transparent = pygame.Surface((board.dims.size, board.dims.size))
        transparent.fill(FADE)
        surface.blit(transparent, (0, board.dims.size + board.margin))

        font = get_font(64)
        word = ""
        if type == 2:
            word = f"TURN {'X' if player == PLAYER_X else 'O'}"
        elif type == 1:
            word = "ULTIMATE WINNER!"
        elif type == 0:
            word = "DRAW"
        lbl = font.render(word, True, CROSS_COLOR)
        surface.blit(lbl,
                     (board.dims.size // 2 - lbl.get_rect().width // 2 + board.margin, board.dims.size + board.margin))

    def draw_player(self, surface, board, player, lb):
        """
        draw a player
        :param surface: current surface
        :param board: current board
        :param player: current player
        :param lb: label
        :return:
        """
        font = get_font(25)
        numricPlayer = 1 if player == PLAYER_X else 2
        figPlayer = 'X' if player == PLAYER_X else 'O'
        lbl = font.render(f'{lb}: {figPlayer}', True, CROSS_COLOR)
        xcor = board.dims.size + board.margin * 3
        ycor = board.margin * 2 + (0 if numricPlayer == 1 else board.margin * 2)
        surface.blit(lbl, (xcor, ycor))
