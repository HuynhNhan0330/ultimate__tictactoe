import random
import math

from const import *


class AI:
    def __init__(self, level=0, player=-1):
        """
        Construct
        :param level: level AI
        :param player: AI player
        """
        self.level = level
        self.player = player

    def rnd(self, board):
        """
        random move
        :param board: current board
        :return: a move
        """
        empty_sqrs = board.get_valids()
        index = random.randrange(0, len(empty_sqrs))

        return empty_sqrs[index]

    def eval(self, board):
        """
        valid move with each algorithm
        :param board: current board
        :return: a move
        """
        if self.level == 0:
            move = self.rnd(board)
        elif self.level == 1:
            minimaxap = Minimaxap(board)
            move = minimaxap.search(board, minimaxap.depth, minimaxap.player)[1]
        elif self.level == 2:
            mcts = MCTS(board)
            move = mcts.search(board, mcts.player)

        return move


class Minimaxap():
    """
    Minimax algorithm and use Alpha – beta pruning
    """

    def __init__(self, board, player=-1, depth=4):
        """
        constructor
        :param board: current board
        :param player: player AI
        :param depth: depth of calculation
        """
        self.board = board
        self.player = player
        self.depth = depth

    def search(self, board, depth, player, alpha=-math.inf, beta=math.inf, isMaximizer=True):
        """
        search the best move
        :param board: current board
        :param depth: depth to search
        :param player: current player
        :param alpha: value alpha
        :param beta: value beta
        :param isMaximizer: True is max else min
        :return: a move
        """
        matrix = []
        for r in range(DIM):
            m = []
            for c in range(DIM):
                m.append(board.squares[r][c].value)
            matrix.append(m)

        if depth == 0 or not board.check_win(matrix) == 2:
            return self.evaluate(board, player), None

        pos = None
        list_valid_move = board.get_valids()

        if isMaximizer:
            maxEval = -math.inf

            for r, c in list_valid_move:
                copyBoard = board.deepcopy()
                value = self.search(copyBoard, depth - 1, -player, alpha, beta, False)[0]

                if value > maxEval:
                    maxEval = value
                    pos = (r, c)

                alpha = max(alpha, value)
                if beta <= alpha:
                    break

            return maxEval, pos

        else:
            minEval = math.inf

            for r, c in list_valid_move:
                copyBoard = board.deepcopy()
                value = self.search(copyBoard, depth - 1, -player, alpha, beta, True)[0]

                if minEval > value:
                    minEval = value
                    pos = (r, c)

                beta = min(beta, value)
                if beta <= alpha:
                    break

            return minEval, pos

    def evaluate(self, board, player):
        """
        calc evaluate value
        :param board: current board
        :param player: current player
        :return: evaluate value
        """
        score = 0
        for r in range(DIM):
            for c in range(DIM):
                if board.squares[r][c].value == 2:
                    score += self.evaluate_sub_board(board.squares[r][c].squares, player)

        return score

    def evaluate_sub_board(self, matrix, player):
        """
        calc score of the board
        :param matrix: current matrix
        :param player: current player
        :return: a score
        """
        score = 0

        # Score row
        for row in matrix:
            score += self.count_score(row, player)

        # Score column
        for col in range(3):
            cols = []
            for row in range(3):
                cols.append(matrix[row][col])

            score += self.count_score(cols, player)

        # Score diagonal
        # asc
        diags = []
        for indx in range(len(matrix)):
            diags.append(matrix[indx][indx])

        score += self.count_score(diags, player)

        # desc
        diags_2 = []
        for indx, rev_indx in enumerate(reversed(range(len(matrix)))):
            diags_2.append(matrix[indx][rev_indx])
        score += self.count_score(diags_2, player)

        if self.board.check_win(matrix) == 0:
            score += 1

        return score

    def count_score(self, array, player):
        """
        Use the formula to calculate the score
        :param array: current array
        :param player: current player
        :return: a score
        """
        opp_player = -player
        score = 0

        if array.count(player) == 3:
            score += 100

        elif array.count(player) == 2:
            score += 50

        elif array.count(player) == 1:
            score += 20

        if array.count(opp_player) == 3:
            score -= 100

        elif array.count(opp_player) == 2:
            score -= 50

        if array.count(player) == 1 and array.count(opp_player) == 2:
            score += 10

        return score


class MCTS:
    """
    Monte Carlo tree search
    rollout improved by Heuristic
    """

    def __init__(self, player=-1, num_nodes=600):
        """
        constructor
        :param player: player AI
        :param num_nodes: number of nodes
        """
        self.player = player
        self.num_nodes = num_nodes
        self.explore_faction = 2

    class Node:
        def __init__(self, parent=None, parent_move=None, move_list=[]):
            """
            constructor
            :param parent: parent node
            :param parent_move: move takes place this node
            :param move_list: move list
            """
            self.parent = parent
            self.parent_move = parent_move
            self.child_nodes = {}  # (Move -> Node) dictionary of children
            self.list_move = move_list
            self.wins = 0  # Total wins
            self.visits = 0  # Total visited.
            self.is_full_expanded = False  # check full expanded

    def calc_ucb(self, node):
        """
        calc ucb value
        :param node: current node
        :return: a ucb value
        """
        # division 0
        if node.visits == 0:
            return float('inf')

        exploit = float(node.wins / node.visits)

        explore = 0
        parent_log = float("-inf")
        if node.parent.visits != 0:
            parent_log = math.log(node.parent.visits)
            explore = self.explore_faction * math.sqrt(parent_log / node.visits)

        return exploit + explore

    def expand_leaf(self, node, board, child_move):
        """
        create a new node
        :param node: current node
        :param board: current board
        :return: a node
        """
        copy_board = board.deepcopy()
        copy_board.mark_sqr(child_move[0], child_move[1], self.player)
        child_list_move = copy_board.get_valids()  # get list move
        child_node = self.Node(node, child_move, child_list_move)
        return child_node

    def select(self, node, board):
        """
        select a node
        :param node: current node
        :param board: current board
        :return: a node
        """
        # child node at 0, UCB at 1
        leaf = (None, None)

        # If node isn't full expanded
        if not node.is_full_expanded:
            for idx in range(min(self.num_nodes, len(node.list_move))):
                child_move = node.list_move[idx]
                child_node = self.expand_leaf(node, board, child_move)
                node.child_nodes[child_move] = child_node
                leaf = (child_node, 0)

            node.is_full_expanded = True
        # Find highest UCB child node
        else:
            for child_key in node.child_nodes.keys():
                child_node = node.child_nodes[child_key]
                child_ucb = self.calc_ucb(child_node)
                if (leaf == (None, None)) or (leaf[1] < child_ucb):
                    leaf = (child_node, child_ucb)

        return leaf[0]

    def rollout(self, board, player):
        """
        the rollout plays out the remainder following a heuristic
        Heuristic: If win, make that move else random move
        :param board: current board
        :param player: current player
        :return: winner
        """
        main_board = board.get_main_board()
        while not board.check_win(main_board) == 2:
            move_list = board.get_valids()
            selected_move = random.choice(move_list)
            score_flags = board.get_score_flags(main_board)

            for move in move_list:
                copy_board = board.deepcopy()
                copy_board.mark_sqr(move[0], move[1], player)
                next_score_flags = copy_board.get_score_flags(copy_board.get_main_board())
                if next_score_flags[player] > score_flags[player]:
                    selected_move = move
                    break

            board.mark_sqr(selected_move[0], selected_move[1], player)
            main_board = board.get_main_board()
            player = -player

        return board.check_win(main_board)

    def backpropagate(self, node, won):
        """
        update values of node
        :param node: current node
        :param won: winner
        :return:
        """
        if not node.parent is None:
            node.visits = node.visits + 1
            if won:
                node.wins = node.wins + 1

            self.backpropagate(node.parent, won)

    def search(self, board, player):
        """
        search best move
        :param board: current board
        :param player: current player
        :return: best move
        """
        root_node = self.Node(None, None, board.get_valids())

        for _ in range(self.num_nodes):
            copy_board = board.deepcopy()
            node = root_node

            leaf = self.select(node, board)
            # simulation
            simulation_result = self.rollout(copy_board, player)
            won = False
            if simulation_result == player:  # win
                won = True

            self.backpropagate(leaf, won)

        # 0 is node, 1 is win rate
        best_node = (None, None)
        for child_key in root_node.child_nodes:
            child_node = root_node.child_nodes[child_key]
            win_rate = child_node.wins / child_node.visits

            if best_node == (None, None) or win_rate > best_node[1]:
                best_node = (child_node, win_rate)

        return best_node[0].parent_move
