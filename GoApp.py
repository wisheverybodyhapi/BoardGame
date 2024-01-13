from BoardGameApp import *

class GoApp(BoardGameApp):
    def __init__(self, board_size=19, current_player=BLACK, history_board=None):
        super().__init__(board_size, current_player, history_board)
        self.game_mode = GO
        self.happen_ko = False
        self.black_capture_count = 0 # 黑方提子数
        self.white_capture_count = 0 # 白方提子数

    def place_piece(self, event):
        self.happen_ko = False

        # 获取落子坐标
        column, row = self.get_click_position(event)

        # 检查是否是合法的落子点
        if not self.is_valid_move(row, column):
            return  # 如果不合法，立即返回

        # 在棋盘上放置棋子并绘制棋子
        self.board[row][column] = self.current_player
        self.draw_stone(row, column)

        # 1. 判断是否是自杀点
        if self.if_suicide(row, column):
            captured_stones = self.capture_stones(row, column)
            print('captured stones:', captured_stones)

            if len(captured_stones) == 0:
                self.game_gui.update_info('{} 坐标 ({},{}) 没气，禁止自杀！'.format(self.current_player, row, column))
                messagebox.showinfo("违规", "禁止出现自杀行为")
                self.board[row][column] = None
                self.game_gui.redraw_board(self.board)
                return
            else: # 虽然无气，但是可以提子，仍旧合法
                if not self.if_happen_ko():
                    opponent = self.get_opponent()
                    captured_stones = [str(s) for s in captured_stones]
                    captured_stones_info = ','.join(captured_stones)
                    self.game_gui.update_info("{} 棋子被提出:{}".format(opponent, captured_stones_info))
        else: # 2. 尝试是否能够正常提子
            captured_stones = self.capture_stones(row, column)
            if captured_stones:
                opponent = self.get_opponent()
                captured_stones = [str(s) for s in captured_stones]
                captured_stones_info = ','.join(captured_stones)
                self.game_gui.update_info("{} 棋子被提出:{}".format(opponent, captured_stones_info))

        # 更新棋盘状态和切换玩家
        if not self.happen_ko:
            # 更新游戏信息
            self.game_gui.update_info(f"玩家 {self.current_player} 落子于 ({row}, {column})")
            self.history_move.append((self.current_player, str(row), str(column)))
            self.update_board_snapshots()
            if self.can_undo < 2:
                self.can_undo += 1
            self.switch_player()
        self.print_board(self.board)

    def get_click_position(self, event):
        column = (event.x - self.game_gui.cell_size // 2) // self.game_gui.cell_size
        row = (event.y - self.game_gui.cell_size // 2) // self.game_gui.cell_size
        return column, row

    def draw_stone(self, row, column):
        if 0 <= column < self.board_size and 0 <= row < self.board_size:
            # 计算棋子的中心位置
            x = (column + 1) * self.game_gui.cell_size
            y = (row + 1) * self.game_gui.cell_size
            draw_color = BLACK if self.board[row][column] == BLACK else WHITE
            # 在交叉点上绘制棋子
            self.game_gui.canvas.create_oval(x - self.game_gui.cell_size // 4, y - self.game_gui.cell_size // 4,
                                    x + self.game_gui.cell_size // 4, y + self.game_gui.cell_size // 4,
                                    fill=draw_color)
                
    def if_happen_ko(self):
        # 判断是否发生了打劫，若发生打劫则恢复棋盘
        if self.is_ko():
            # 如果是打劫，撤销刚才的落子，恢复棋盘
            messagebox.showinfo("违规", "禁止出现打劫行为")
            self.board = copy.deepcopy(self.last_1_board)
            self.game_gui.redraw_board(self.board)
            self.happen_ko = True
            return True
        return False

    def is_ko(self):
        # 实现检查打劫的逻辑
        if self.board == self.last_2_board:
            return True
        return False

    # 判断是否是自杀点
    def if_suicide(self, x, y, checked=None):
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
                    elif self.board[nx][ny] == current_player and not self.if_suicide(nx, ny, checked):
                        return False  # 相邻同色棋子组有气
        return True  # 没有找到空点，没有气，是死棋

    def capture_stones(self, row, column):
        # 存储被提走的棋子位置
        captured_positions = []

        # 检查每个邻近点是否有对方的棋子，并且是否被围死
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = row + dx, column + dy
            if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                if self.board[nx][ny] is not None and self.board[nx][ny] != self.current_player:
                    if self.if_suicide(nx, ny):
                        # 如果对方的棋子被围死，提走这些棋子
                        captured_positions += self.remove_stones(nx, ny)
                        # 更新提子计数器
                        if self.current_player == BLACK:
                            self.black_capture_count += len(captured_positions)
                        else:
                            self.white_capture_count += len(captured_positions)


        return captured_positions

    def remove_stones(self, x, y):
        # 从棋盘上移除被围死的棋子，并返回被移除的棋子位置列表
        removed_positions = []
        opponent = self.get_opponent()
        stack = [(x, y)]
        while stack:
            x, y = stack.pop()
            if 0 <= x < self.board_size and 0 <= y < self.board_size and self.board[x][y] == opponent:
                self.board[x][y] = None  # 移除棋子
                removed_positions.append((x, y))
                stack.extend([(x-1, y), (x+1, y), (x, y-1), (x, y+1)])
        self.game_gui.redraw_board(self.board)
        return removed_positions
            
    def quit_move(self):
        # 放弃此步
        self.game_gui.update_info("{}放弃此步".format(self.current_player))
        self.switch_player()

    def judge_win(self):
        # 根据围棋的数子法来计算分数
        black_territory, white_territory = self.calculate_territory()
        black_captures = self.black_capture_count  # 黑方提子数
        white_captures = self.white_capture_count  # 白方提子数

        komi = 0  # 贴目，这个值可能根据规则有所不同
        black_score = black_territory + black_captures - komi
        white_score = white_territory + white_captures
        self.game_gui.update_info('黑方提子数{}，黑方领地面积{}，黑方分数{}'.format(black_captures,
                                    black_territory, black_score))
        self.game_gui.update_info('白方提子数{}，白方领地面积{}，白方分数{}'.format(white_captures,
                                    white_territory, white_score))
        winner = None
        if black_score > white_score:
            winner = BLACKPLAYER
        elif white_score > black_score:
            winner = WHITEPLAYER
        else:
            winner = '平局'
        self.game_gui.update_info("黑方让子{}子，玩家 {} 胜利！游戏结束！".format(komi, winner))
        self.game_gui.update_info(f"玩家 {winner} 胜利！游戏结束！")
        messagebox.showinfo("游戏结束", f"{winner} 赢了！")
        self.game_over = True

    def calculate_territory(self):
        black_territory = 0
        white_territory = 0
        visited = set()

        for x in range(self.board_size):
            for y in range(self.board_size):
                if self.board[x][y] is None and (x, y) not in visited:
                    territory, area = self.flood_fill_territory(x, y, visited)
                    if territory == BLACK:
                        black_territory += area
                    elif territory == WHITE:
                        white_territory += area
                    # 争议区域不计入任何一方

        return black_territory, white_territory

    def flood_fill_territory(self, x, y, visited):
        stack = [(x, y)]
        territory = None
        area = 0

        while stack:
            x, y = stack.pop()
            if (x, y) in visited or not (0 <= x < self.board_size and 0 <= y < self.board_size):
                continue

            visited.add((x, y))

            if self.board[x][y] is None:
                area += 1
                neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
                for nx, ny in neighbors:
                    if (nx, ny) not in visited:
                        stack.append((nx, ny))
            else:
                if territory is None:
                    territory = self.board[x][y]
                elif territory != self.board[x][y]:
                    territory = None  # 如果发现有不同颜色的棋子，则该区域为争议区

        return territory, area
