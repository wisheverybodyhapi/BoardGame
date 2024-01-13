from BoardGameApp import *

class GomokuApp(BoardGameApp):
    def __init__(self, board_size=15, current_player=BLACK, history_board=None):
        super().__init__(board_size, current_player, history_board)
        self.game_mode = GOMOKU

    def place_piece(self, event):
        """五子棋落子"""
        column = (event.x - self.game_gui.cell_size // 2) // self.game_gui.cell_size
        row = (event.y - self.game_gui.cell_size // 2) // self.game_gui.cell_size
        if 0 <= column < self.board_size and 0 <= row < self.board_size:
            # 计算棋子的中心位置
            x = (column + 1) * self.game_gui.cell_size
            y = (row + 1) * self.game_gui.cell_size
        # 基本的落子逻辑
        if self.is_valid_move(row, column):
            self.board[row][column] = self.current_player
            draw_color = BLACK if self.current_player == BLACK else WHITE
            self.history_move.append((self.current_player, row, column))
            # 在交叉点上绘制棋子
            self.game_gui.canvas.create_oval(x - self.game_gui.cell_size // 4, y - self.game_gui.cell_size // 4,
                                    x + self.game_gui.cell_size // 4, y + self.game_gui.cell_size // 4,
                                    fill=draw_color)
            # 更新游戏信息
            self.game_gui.update_info(f"玩家 {self.current_player} 落子于 ({row}, {column})")

            if self.can_undo < 2:
                self.can_undo += 1

            if self.check_win(row, column):
                winner = BLACKPLAYER if self.current_player == BLACK else WHITEPLAYER
                self.game_gui.update_info(f"玩家 {winner} 胜利！游戏结束！")
                messagebox.showinfo("游戏结束", f"{winner} 赢了！")
                self.game_over = True
            else:
                self.update_board_snapshots()
                self.switch_player()

    def check_win(self, x, y):
        # 实现五子棋的胜利条件检查
        def count_stones(dx, dy):
            count = 0
            i, j = x + dx, y + dy
            while 0 <= i < self.board_size and 0 <= j < self.board_size and self.board[i][j] == self.current_player:
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
