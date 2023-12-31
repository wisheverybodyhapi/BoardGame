from BoardGameApp import *
import copy

class GoApp(BoardGameApp):
    def __init__(self, board_size=19, current_player='Black', history_board=None):
        super().__init__(board_size, current_player, history_board)
        self.game_mode = 'go'
        self.last_move = None
        self.happen_ko = False
        self.black_capture_count = 0 # 黑方提子数
        self.white_capture_count = 0 # 白方提子数

    def place_piece(self, event):
        # 围棋的落子规则
        column = (event.x - self.game_gui.cell_size // 2) // self.game_gui.cell_size
        row = (event.y - self.game_gui.cell_size // 2) // self.game_gui.cell_size
        if 0 <= column < self.board_size and 0 <= row < self.board_size:
            # 计算棋子的中心位置
            x = (column + 1) * self.game_gui.cell_size
            y = (row + 1) * self.game_gui.cell_size
        # 基本的落子逻辑
        if not self.game_over and self.board[row][column] is None:
            # 更新游戏信息
            self.game_gui.update_info(f"玩家 {self.current_player} 落子于 ({row}, {column})")
            self.board[row][column] = self.current_player
            self.check_state(row, column)

            if not self.happen_ko:
                self.update_board_snapshots()
            draw_color = "black" if self.board[row][column] == "Black" else "white"
            # 在交叉点上绘制棋子
            self.game_gui.canvas.create_oval(x - self.game_gui.cell_size // 4, y - self.game_gui.cell_size // 4,
                                    x + self.game_gui.cell_size // 4, y + self.game_gui.cell_size // 4,
                                    fill=draw_color)
            self.game_gui.redraw_board(self.board)
            # 更新游戏信息
            self.history_move.append((self.current_player, str(row), str(column)))
            if self.can_undo < 2:
                self.can_undo += 1

            if not self.happen_ko:
                self.switch_player()
                
        

    def if_dead(self, x, y, checked=None):
        if checked is None:
            checked = set()

        current_player = self.board[x][y]
        checked.add(current_player)

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                if (nx, ny) not in checked:
                    checked.add((x, y))
                    if self.board[nx][ny] is None:
                        return False  # 找到一个空点，有气
                    elif self.board[nx][ny] == current_player and not self.if_dead(nx, ny, checked):
                        return False  # 相邻同色棋子组有气
        self.game_gui.update_info('{}坐标({},{})没气了'.format(self.board[x][y], x, y))
        return True  # 没有找到空点，没有气，是死棋


    def check_state(self, last_x, last_y):
        # 检查是否有棋子被围死
        captured_positions = self.capture_stones(last_x, last_y)
        if captured_positions:
            # 如果有棋子被提走，更新棋盘并检查是否是打劫的情况
            self.update_board(captured_positions)
            if self.is_ko(last_x, last_y, captured_positions):
                # 如果是打劫，撤销刚才的落子
                self.board = self.last_1_board
                messagebox.showinfo("打劫", "禁止出现该种情况")
                self.happen_ko = True
            else:
                self.happen_ko = False

    def is_ko(self, last_x, last_y, captured_positions):
        # 实现检查打劫的逻辑
        # 简单的实现可以是检查是否只提走了一个棋子，并且现在落子会复原上一手的局面
        if len(captured_positions) == 1:
            return self.board == self.last_2_board
            # 检查上一手是否只有一个棋子被提走，并且现在的落子会立即复原局面
        return False

    def update_board(self, captured_positions):
        # 更新棋盘状态，移除被提走的棋子
        for x, y in captured_positions:
            self.board[x][y] = None
        self.game_gui.redraw_board(self.board)

    def capture_stones(self, last_x, last_y):
        # 存储被提走的棋子位置
        captured_positions = []

        # 检查每个邻近点是否有对方的棋子，并且是否被围死
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = last_x + dx, last_y + dy
            if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                if self.board[nx][ny] is not None and self.board[nx][ny] != self.current_player:
                    if self.if_dead(nx, ny):
                        # 如果对方的棋子被围死，提走这些棋子
                        captured_positions += self.remove_stones(nx, ny)
                        # 更新提子计数器
                        if self.current_player == "Black":
                            self.white_capture_count += len(captured_positions)
                        else:
                            self.black_capture_count += len(captured_positions)

        return captured_positions

    def remove_stones(self, x, y):
        # 从棋盘上移除被围死的棋子，并返回被移除的棋子位置列表
        removed_positions = []
        opponent = self.board[x][y]
        stack = [(x, y)]
        while stack:
            x, y = stack.pop()
            if 0 <= x < self.board_size and 0 <= y < self.board_size and self.board[x][y] == opponent:
                self.board[x][y] = None  # 移除棋子
                removed_positions.append((x, y))
                stack.extend([(x-1, y), (x+1, y), (x, y-1), (x, y+1)])

        return removed_positions
            
    def judge_win(self):
        # 根据棋子占地面积以及提子数来计算分数
        black_territory = 0
        white_territory = 0
        black_captures = self.black_capture_count  # 黑方提子数
        white_captures = self.white_capture_count  # 白方提子数

        for x in range(self.board_size):
            for y in range(self.board_size):
                if self.board[x][y] is None:
                    territory_owner = self.check_territory(x, y)
                    if territory_owner == "Black":
                        black_territory += 1
                    elif territory_owner == "White":
                        white_territory += 1

        black_score = black_territory + black_captures
        white_score = white_territory + white_captures

        winner = None
        if black_score > white_score:
            winner = "Black"
        elif white_score > black_score:
            winner = "White"
        else:
            winner = "Draw"
        
        self.game_gui.update_info(f"玩家 {winner} 胜利！游戏结束！")
        messagebox.showinfo("游戏结束", f"{winner} 赢了！")
        self.game_over = True

    def check_territory(self, x, y):
        visited = set()
        return self.flood_fill(x, y, visited)

    def flood_fill(self, x, y, visited):
        if (x, y) in visited or not (0 <= x < self.board_size and 0 <= y < self.board_size):
            return None
        visited.add((x, y))

        if self.board[x][y] is not None:
            return self.board[x][y]  # 遇到棋子，返回棋子颜色

        neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        owner = None
        for nx, ny in neighbors:
            if (nx, ny) not in visited:
                neighbor_owner = self.flood_fill(nx, ny, visited)
                if neighbor_owner is None:
                    continue
                if owner is None:
                    owner = neighbor_owner
                elif owner != neighbor_owner:
                    return None  # 如果邻居属于不同玩家，该区域为争议区

        return owner