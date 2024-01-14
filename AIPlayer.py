import random
from Config import *

class AIPlayer:
    def __init__(self, level, current_game, name='电脑玩家'):
        self.level = level
        self.name = name
        self.current_game = current_game
        self.current_move = None
        self.center_position = (current_game.board_size // 2, current_game.board_size // 2)

    def make_move(self):
        board = self.current_game.board
        current_stone = self.current_game.current_stone

        if self.level == EASY:
            self.current_move = self.random_move(board, current_stone)
        elif self.level == MEDIUM:
            self.current_move = self.rule_based_move(board, current_stone)
            
        row, column = self.current_move
        self.current_game.place_piece(row, column)

    def random_move(self, board, current_stone):
        # 一级AI落子算法
        valid_moves = self.get_valid_moves(board, current_stone)
        return random.choice(valid_moves) if valid_moves else None


    def rule_based_move(self, board, current_stone):
        # 二级AI落子算法
        # 获取所有合法落子位置
        valid_moves = self.get_valid_moves(board, current_stone)

        # 如果没有合法落子位置，返回None
        if not valid_moves:
            return None

        # 优先级规则：阻止对手连珠 > 形成自己的连珠
        opponent_stone = WHITE if current_stone == BLACK else BLACK
        best_move = []
        max_score = -1

        for move in valid_moves:
            score = self.evaluate_move(board, move, current_stone, opponent_stone)
            if score > max_score:
                max_score = score
                best_move = []
                best_move.append(move)
            elif score == max_score:
                best_move.append(move)

        return self.center_position if self.center_position in best_move else random.choice(best_move)

    def evaluate_move(self, board, move, current_stone, opponent_stone):
        row, col = move
        score = 0

        # 定义检查方向：水平、垂直、两个对角线
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for dr, dc in directions:
            score += self.check_line(board, row, col, dr, dc, current_stone, opponent_stone)

        return score

    def check_line(self, board, row, col, dr, dc, current_stone, opponent_stone):
        line_score = 0
        count_current = 0
        count_opponent = 0

        # 检查落子点在当前方向上当前棋子的连珠情况（遇到敌方棋子或者空白，就退出）
        for i in range(1, 5):
            r, c = row + dr * i, col + dc * i
            if 0 <= r < len(board) and 0 <= c < len(board[r]):
                if board[r][c] == current_stone:
                    count_current += 1
                else:
                    break
            else:
                break

        # 反向检查
        for i in range(1, 5):
            r, c = row - dr * i, col - dc * i
            if 0 <= r < len(board) and 0 <= c < len(board[r]):
                if board[r][c] == current_stone:
                    count_current += 1
                else:
                    break
            else:
                break

        # 检查落子点在当前方向上对方棋子的连珠情况（遇到敌方棋子或者空白，就退出）
        for i in range(1, 5):
            r, c = row + dr * i, col + dc * i
            if 0 <= r < len(board) and 0 <= c < len(board[r]):
                if board[r][c] == opponent_stone:
                    count_opponent += 1
                else:
                    break
            else:
                break

        # 反向检查
        for i in range(1, 5):
            r, c = row - dr * i, col - dc * i
            if 0 <= r < len(board) and 0 <= c < len(board[r]):
                if board[r][c] == opponent_stone:
                    count_opponent += 1
                else:
                    break
            else:
                break

        # 根据连珠数量给分
        if count_current == 1:
            line_score = 2      # 形成2连珠
        elif count_current == 2:
            line_score = 50     # 形成3连珠
        elif count_current == 3:
            line_score = 300    # 形成4连珠
        elif count_current >= 4:
            line_score = 10000  # 形成5连珠或以上
    
        if count_opponent == 1:
            line_score = 1      # 阻止对手形成2连珠
        elif count_opponent == 2:
            line_score = 40     # 阻止对手形成3连珠
        elif count_opponent == 3:
            line_score = 200    # 阻止对手形成4连珠
        elif count_opponent == 4:
            line_score = 5000   # 阻止对手形成5连珠

        return line_score


    def get_valid_moves(self, board, current_stone):
        valid_moves = []
        for row in range(len(board)):
            for col in range(len(board[row])):
                if self.is_valid_move(board, row, col, current_stone):
                    valid_moves.append((row, col))
        return valid_moves

    def is_valid_move(self, board, row, column, current_stone):
        board_size = len(board)
        if not self.current_game.game_over and 0 <= row < board_size and 0 <= column < board_size and self.current_game.board[row][column] is None:
            return True
        return False
