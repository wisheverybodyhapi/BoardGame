from BoardGameApp import *

class GomokuApp(BoardGameApp):
    def __init__(self, board_size, current_stone=BLACK, history_board=None, versus_mode=None, difficulty=None, difficulty2=None):
        super().__init__(board_size, current_stone, history_board, versus_mode, difficulty, difficulty2)
        self.game_mode = GOMOKU
        self.game_pattern = GOMOKUPATTERN

    def place_piece(self, row, column, current_player, current_stone):
        """五子棋落子"""
        # 检查是否是合法的落子点
        if not self.is_valid_move(row, column):
            return False # 如果不合法，立即返回

        # 在棋盘上放置棋子并绘制棋子
        self.board[row][column] = current_stone
        self.draw_stone(row, column, current_stone)

        self.history_move.append((PLACESTONE, current_player, current_stone, row, column))

        # 更新游戏信息
        self.game_gui.update_info(f"玩家 {current_player} 落子于 ({row}, {column})")
        
        if self.can_undo < 2:
            self.can_undo += 1

        if self.check_win(row, column):
            winner = current_player
            self.game_gui.update_info(f"玩家 {winner} 胜利！游戏结束！")
            messagebox.showinfo("游戏结束", f"{winner} 赢了！")
            self.game_over = True
            self.handle_game_end()
        else:
            self.update_board_snapshots()
            self.switch_player()
        return True

    def check_win(self, x, y):
        # 实现五子棋的胜利条件检查
        def count_stones(dx, dy):
            count = 0
            i, j = x + dx, y + dy
            while 0 <= i < self.board_size and 0 <= j < self.board_size and self.board[i][j] == self.current_stone:
                count += 1
                i += dx
                j += dy
            return count

        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dx, dy in directions:
            if count_stones(dx, dy) + count_stones(-dx, -dy) >= 4:
                return True

        return False

    # 其他五子棋特有的方法...
