from BoardGameApp import *

class ReversiApp(BoardGameApp):

    def __init__(self, board_size, current_stone=BLACK, history_board=None, versus_mode=None, difficulty=None):
        super().__init__(board_size, current_stone, history_board, versus_mode, difficulty)
        self.game_mode = REVERSI
        self.game_pattern = 'reversi'
        self.init_board()

    def init_board(self):
        # 初始化棋盘中央的四个棋子
        self.board[4][4], self.board[5][5] = WHITE, WHITE
        self.board[5][4], self.board[4][5] = BLACK, BLACK
        self.draw_stone(4, 4)
        self.draw_stone(4, 5)
        self.draw_stone(5, 4)
        self.draw_stone(5, 5)
        
    def place_piece(self, row, column):

        # 检查是否是合法的落子点
        if not self.is_valid_move(row, column):
            return False # 如果不合法，立即返回
        
        # 先下棋，后判断
        self.board[row][column] = self.current_stone

        self.history_move.append((PLACESTONE, self.current_player.name, self.current_stone, row, column))

        # 实现翻转对方棋子的逻辑，判断能否翻转对手棋子
        has_filp = self.flip_opponent_pieces(row, column, self.current_stone)

        if has_filp:
            # 在棋盘上放置棋子并绘制棋子
            self.draw_stone(row, column)
            self.game_gui.update_info(f"玩家 {self.current_player.name} 落子于 ({row}, {column})")
            self.switch_player()
        else:
            # 否则恢复棋盘
            self.game_gui.update_info(f"玩家 {self.current_player.name} 在({row}, {column})无子可落")
            self.board[row][column] = None
        return True

    def flip_opponent_pieces(self, row, col, player):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]
        opponent = WHITE if player == BLACK else BLACK
        all_pieces_to_flip = []
        has_flip = False
        for dr, dc in directions:
            r, c = row + dr, col + dc
            pieces_to_flip = []
            
            while 1 <= r < 9 and 1 <= c < 9 and self.board[r][c] == opponent:
                has_flip = True
                pieces_to_flip.append((r, c))
                r += dr
                c += dc
            
            if 1 <= r < 9 and 1 <= c < 9 and self.board[r][c] == player:
                for piece_row, piece_col in pieces_to_flip:
                    self.board[piece_row][piece_col] = player
                    self.draw_stone(piece_row, piece_col)
            all_pieces_to_flip = all_pieces_to_flip + pieces_to_flip
        
        flip_info = ','.join([str(e) for e in all_pieces_to_flip])
        if all_pieces_to_flip:
            self.game_gui.update_info("{} {} 被翻转".format(self.get_opponent(), flip_info))
        return has_flip

    def get_click_position(self, event):
        column = (event.x) // self.game_gui.cell_size
        row = (event.y) // self.game_gui.cell_size
        return row, column

    def is_valid_move(self, row, column):
        if not self.game_over and 1 <= row < self.board_size and 1 <= column < self.board_size and self.board[row][column] is None:
            return True
        return False

    def judge_win(self):
        # 计算
        black_count = sum(row.count(BLACK) for row in self.board)
        white_count = sum(row.count(WHITE) for row in self.board)
        winner = None
        if black_count > white_count:
            winner = self.BLACKPLAYER.name
        elif white_count > black_count:
            winner = self.WHITEPLAYER.name
        else:
            winner = 'Draw'
        
        self.game_gui.update_info("黑子{}，白子{}，玩家 {} 胜利！游戏结束！".format(black_count, white_count, winner))
        messagebox.showinfo("游戏结束", f"{winner} 赢了！")
        self.game_over = True
        self.handle_game_end()

    def draw_stone(self, row, column):
        if 0 <= column < self.board_size and 0 <= row < self.board_size:
            # 计算棋子的中心位置
            x = column * self.game_gui.cell_size + self.game_gui.cell_size // 2
            y = row * self.game_gui.cell_size + self.game_gui.cell_size // 2
            draw_color = BLACK if self.board[row][column] == BLACK else WHITE
            
            if self.arrow:
                self.game_gui.canvas.delete(self.arrow)

            # 在交叉点上绘制棋子
            self.game_gui.canvas.create_oval(x - self.game_gui.cell_size // 4, y - self.game_gui.cell_size // 4,
                                             x + self.game_gui.cell_size // 4, y + self.game_gui.cell_size // 4,
                                             fill=draw_color)
            self.arrow = self.game_gui.canvas.create_line(x + 10, y + 10, x, y, arrow=LAST, fill="red")


