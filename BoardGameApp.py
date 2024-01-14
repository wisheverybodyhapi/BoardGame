from GameGUI import *
import copy
from Config import *
from HumanPlayer import *
from AIPlayer import *

class BoardGameApp:
    def __init__(self, board_size, current_stone=BLACK, history_board=None, versus_mode=None, difficulty=None, difficulty2=None):
        self.game_gui = GameGUI(board_size)
        self.board_size = board_size
        self.game_type = None
        self.game_over = False
        self.game_mode = None
        self.game_pattern = None
        self.versus_mode = versus_mode
        self.difficulty = difficulty
        self.difficulty2 = difficulty2

        self.can_undo = 0
        self.history_move = []
        self.current_stone = current_stone
        self.board = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]

        # 拷贝三份棋盘“快照”，悔棋和判断“打劫”时需要作参考
        self.last_3_board = copy.deepcopy(self.board)
        self.last_2_board = copy.deepcopy(self.board)
        self.last_1_board = copy.deepcopy(self.board)

        # 如果是加载存档，那么需要加载历史棋盘重新绘制
        if history_board != None:
            self.load_game(history_board)

        self.game_gui.create_buttons(self.give_up, self.undo_move, self.save_game, self.quit_game, self.judge_win, self.quit_move)

        # 根据对战模式初始化玩家
        self.player_1 = None
        self.player_2 = None
        self.initialize_players(versus_mode)
    
        # 总是黑棋先手，随机选择一名玩家为
        self.BLACKPLAYER = random.choice([self.player_1, self.player_2])
        self.WHITEPLAYER = self.player_1 if self.BLACKPLAYER == self.player_2 else self.player_2

        self.current_player = self.BLACKPLAYER
        self.BLACKPLAYER = self.BLACKPLAYER
        self.WHITEPLAYER = self.WHITEPLAYER

        self.game_gui.update_info("{}执黑子，{}执白子".format(self.BLACKPLAYER.name, self.WHITEPLAYER.name))
        self.game_gui.update_info("黑子先行，比赛开始！")
        
        self.arrow = None
        self.start_game()
    
    def initialize_players(self, versus_mode):
        if versus_mode == PVC:
            self.player_1 = HumanPlayer(self)
            self.player_2 = AIPlayer(self.difficulty, self)
        elif versus_mode == CVC:
            self.player_1 = AIPlayer(self.difficulty, self, name=self.get_ai_name(difficulty=self.difficulty))
            self.player_2 = AIPlayer(self.difficulty2, self, name=self.get_ai_name(difficulty2=self.difficulty2))
        elif versus_mode == PVP:
            self.player_1 = HumanPlayer()
            # self.player_2 = NetworkPlayer(self.network_manager)
        elif versus_mode == SP:
            self.player_1 = HumanPlayer(self, 'gfc')
            self.player_2 = HumanPlayer(self, 'mxy')

    def get_ai_name(self, difficulty=None, difficulty2=None):
        ai_name = None

        if difficulty == EASY:
            ai_name = '简单电脑1'
        elif difficulty == MEDIUM:
            ai_name =  '中等电脑1'

        if difficulty2 == EASY:
            ai_name = '简单电脑2'
        elif difficulty2 == MEDIUM:
            ai_name =  '中等电脑2'

        return ai_name
    
    def start_game(self):
        if self.versus_mode == PVC:
            self.handle_player_vs_ai()
        elif self.versus_mode == CVC:
            self.handle_ai_vs_ai()
        elif self.versus_mode == PVP:
            self.handle_online_game()
        elif self.versus_mode == SP:
            self.handle_single_player_mode()

    def handle_player_vs_ai(self):
        # 如果当前玩家是AI，则立即执行AI的落子
        if isinstance(self.current_player, AIPlayer):
            self.current_player.make_move()
            
    def handle_ai_vs_ai(self):
        if not self.game_over:
            self.current_player.make_move()


    def handle_online_game(self):
        # 实现联机对战
        pass

    def handle_single_player_mode(self):
        # 实现单人模式
        pass

    # 立刻认输button
    def give_up(self):
        if not self.game_over:
            self.history_move.append((GIVEUP, self.current_player.name, self.current_stone))
            loser = self.current_stone
            winner = self.WHITEPLAYER if loser == BLACK else self.BLACKPLAYER
            messagebox.showinfo("游戏结束", f"{loser} 认输了，{winner} 赢了！")
            self.game_gui.update_info(f"{loser} 认输了。")
            self.game_over = True
            self.handle_game_end()

    def handle_game_end(self):
        # 处理游戏终局的函数
        # 1. 保存录像
        # 获取当前时间的时间戳
        current_time = time.time()

        # 将时间戳转换为时间结构
        time_struct = time.localtime(current_time)

        # 自定义时间格式
        formatted_time = time.strftime("%Y_%m_%d_%H_%M_%S", time_struct)
        record_file = '{}_record.txt'.format(formatted_time)
        with open(record_file, "w", encoding='utf-8') as file:
            for historymove in self.history_move:
                file.write(str(historymove) + '\n')
            

    # 悔棋button
    def undo_move(self):
        if self.can_undo == 2 and not self.game_over:
            self.board = self.last_3_board
            self.update_board_snapshots()
            self.game_gui.clear_board()
            self.game_gui.redraw_board(self.board)
            self.game_gui.update_info(self.current_stone + '要求悔棋一步，两回合内不再能悔棋！')
            self.can_undo = 0
            self.history_move.append((UNDOMOVE, self.current_player.name, self.current_stone))

    # 保存游戏button
    def save_game(self):
        if self.game_over:
            messagebox.showinfo("提示", "游戏已结束，无需保存。")
            return
        # 列出所有符合当前游戏模式的存档文件
        # print('self.game_mode', self.game_mode)
        pattern = "gomoku_" if self.game_mode == GOMOKU else "go_"
        files = [f for f in os.listdir() if f.startswith(pattern) and f.endswith('.txt')]
        # print('files:', files, len(files))
        save_file = "{}save_{}.txt".format(pattern, len(files))
        # print('save_file:', save_file)
        with open(save_file, "w") as file:
            file.write(str(self.board_size) + "\n")
            file.write(self.current_stone + "\n")
            for i in range(len(self.board)):
                row = self.board[i]
                for j in range(len(row)):
                    e = row[j]
                    if e != None:
                        file.write("{} {} {}\n".format(e, i, j))
                        
        messagebox.showinfo("游戏保存", "游戏已保存！")

    # 判断胜负button
    def judge_win(self):
        pass

    # 放弃此步button
    def quit_move(self):
        pass
    
    # 退出游戏button
    def quit_game(self):
        exit()

    def switch_player(self):
        self.current_stone = WHITE if self.current_stone == BLACK else BLACK
        self.current_player = self.WHITEPLAYER if self.current_player == self.BLACKPLAYER else self.BLACKPLAYER
        if isinstance(self.current_player, AIPlayer):
            self.game_gui.canvas.after(1000, self.current_player.make_move)  # 1秒后再次调用
            


    def load_game(self, board):
        self.board = board
        self.game_gui.redraw_board(board)


    def get_opponent(self):
        opponent = WHITE if self.current_stone == BLACK else BLACK
        return opponent

    def update_board_snapshots(self):
        self.last_3_board = copy.deepcopy(self.last_2_board)
        self.last_2_board = copy.deepcopy(self.last_1_board)
        self.last_1_board = copy.deepcopy(self.board)

    def is_valid_move(self, row, column):
        if not self.game_over and 0 <= row < self.board_size and 0 <= column < self.board_size and self.board[row][column] is None:
            return True
        return False

    def draw_stone(self, row, column):
        if 0 <= column < self.board_size and 0 <= row < self.board_size:
            # 计算棋子的中心位置
            x = (column + 1) * self.game_gui.cell_size
            y = (row + 1) * self.game_gui.cell_size
            draw_color = BLACK if self.board[row][column] == BLACK else WHITE

            if self.arrow:
                self.game_gui.canvas.delete(self.arrow)
            # 在交叉点上绘制棋子
            self.game_gui.canvas.create_oval(x - self.game_gui.cell_size // 4, y - self.game_gui.cell_size // 4,
                                    x + self.game_gui.cell_size // 4, y + self.game_gui.cell_size // 4,
                                    fill=draw_color)
            self.arrow = self.game_gui.canvas.create_line(x + 10, y + 10, x, y, arrow=LAST, fill="red")

    def get_click_position(self, event):
        column = (event.x - self.game_gui.cell_size // 2) // self.game_gui.cell_size
        row = (event.y - self.game_gui.cell_size // 2) // self.game_gui.cell_size
        return row, column

    def place_piece(self, row, column):
        # 落子规则需具体实现
        pass

    def check_win(self, x, y):
        # 检查胜利条件
        pass
    
    # 用于悔棋后，进行的棋盘状态恢复
    def restore_game(self):
        pass

    def print_board(self, board):
        for row in board:
            for c in row:
                print(c, end='\t')
            print()
