from GoApp import *
from GomokuApp import *
from Reversi import *
from AIPlayer import *
from HumanPlayer import *

class SettingGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("请选择游戏模式：")
        self.width = 350
        self.height = 250
        self.button_width = 10
        self.button_height = 2
        self.game_mode = None
        self.game_type = None
        self.board_size = None
        self.versus_mode = None
        self.difficulty = None
        self.difficulty2 = None
        self.window.geometry("{}x{}+0+0".format(self.width, self.height))

        # 游戏模式选择按钮
        self.button_gomoku = tk.Button(self.window, text=GOMOKU, command=lambda: self.select_game_mode(GOMOKU), width=self.button_width, height=self.button_height)
        self.button_gomoku.pack()

        self.button_go = tk.Button(self.window, text=GO, command=lambda: self.select_game_mode(GO), width=self.button_width, height=self.button_height)
        self.button_go.pack()

        self.button_reversi = tk.Button(self.window, text=REVERSI, command=lambda: self.select_game_mode(REVERSI), width=self.button_width, height=self.button_height)
        self.button_reversi.pack()

    def select_game_mode(self, game_mode):
        self.game_mode = game_mode
        self.button_gomoku.pack_forget()
        self.button_go.pack_forget()
        self.button_reversi.pack_forget()


        # 游戏类型选择按钮
        self.button_new_game = tk.Button(self.window, text="新游戏", command=lambda: self.select_game_type("新游戏"), width=self.button_width, height=self.button_height)
        self.button_new_game.pack()

        self.button_load_history = tk.Button(self.window, text="加载存档", command=lambda: self.select_game_type("加载存档"), width=self.button_width, height=self.button_height)
        self.button_load_history.pack()

        self.button_replay = tk.Button(self.window, text="回放录像", command=lambda: self.replay(), width=self.button_width, height=self.button_height)
        self.button_replay.pack()

    def select_game_type(self, game_type):
        self.game_type = game_type
        self.button_new_game.pack_forget()
        self.button_load_history.pack_forget()
        self.button_replay.pack_forget()

        if self.game_type == "新游戏":
            self.choose_versus_mode()
        elif self.game_type == "加载存档":
            self.load_game()

    def replay(self):
        self.button_new_game.pack_forget()
        self.button_load_history.pack_forget()
        self.button_replay.pack_forget()
        # 实现回放录像功能
        pattern = None

        if self.game_mode == GOMOKU:
            pattern = GOMOKUPATTERN
        elif self.game_mode == GO:
            pattern = GOPATTERN
        elif self.game_mode == REVERSI:
            pattern = REVERSIPATTERN
            
        print('pattern', pattern)
        # 1. 列出所有录像文件
        record_files = [f for f in os.listdir('.') if f.startswith(pattern + '_') and f.endswith('_record.txt')]
        if not record_files:
            messagebox.showinfo("回放录像", "没有找到录像文件")
            self.window.destroy()
            return

        # 创建一个新窗口来显示录像文件列表
        self.replay_window = tk.Toplevel(self.window)
        self.replay_window.title("选择录像文件")
        self.replay_window.geometry("300x250+{}+{}".format(self.width, 0))

        # 创建一个Listbox来列出文件
        listbox = tk.Listbox(self.replay_window)
        listbox.pack(fill=tk.X)  # 仅水平填充，不扩展
        listbox.pack()

        # 填充Listbox
        for file in record_files:
            listbox.insert(tk.END, file)

        # 创建一个按钮来选择文件
        select_button = tk.Button(self.replay_window, text="选择", command=lambda: self.load_replay(listbox.get(tk.ACTIVE)))
        select_button.pack()
        
    def load_replay(self, record_file):
        self.replay_window.destroy()
        self.window.destroy()
        # 加载并回放选中的录像
        print("选择的录像文件：", record_file)

        # 加载和回放录像的逻辑
        with open(record_file, 'r', encoding='utf-8') as file:
            record_contents = file.readlines()
            board_size = int(record_contents[0])

            app = None
            if self.game_mode == GOMOKU:
                app = GomokuApp(board_size)
            elif self.game_mode == GO:
                app = GoApp(board_size)
            elif self.game_mode == REVERSI:
                app = ReversiApp(board_size)

        app.game_gui.window.after(1000, lambda: self.replay_step(app, record_contents, 1))
        app.game_gui.run()

    def replay_step(self, app, record_contents, index):
        print(f"Replaying step {index}")  # 调试信息
        if index < len(record_contents):
            record_line = record_contents[index]
            record = record_line.strip('()\n').split(',')
            opnd = int(record[0])
            
            if opnd == PLACESTONE:
                current_player, current_stone, row, column = record[1:]
                row = int(row)
                column = int(column)
            elif opnd == GIVEUP:
                current_player, current_stone = record[1:]
                
                
            current_player = current_player.strip("' ")
            current_stone = current_stone.strip("' ")

            if opnd == PLACESTONE:
                app.place_piece(row, column, current_player, current_stone)
            elif opnd == GIVEUP:
                app.give_up(current_player, current_stone)

            
            app.game_gui.window.after(1000, lambda: self.replay_step(app, record_contents, index + 1))

    def choose_versus_mode(self):
        self.versus1_button = tk.Button(self.window, text="联机对战", command=lambda: self.select_versus_mode(PVP), width=self.button_width, height=self.button_height)
        self.versus1_button.pack()
        if self.game_mode == GOMOKU: # 只有五子棋有AI玩家功能
            self.versus2_button = tk.Button(self.window, text="人机对战", command=lambda: self.select_versus_mode(PVC), width=self.button_width, height=self.button_height)
            self.versus2_button.pack()
            self.versus3_button = tk.Button(self.window, text="AIvsAI模式", command=lambda: self.select_versus_mode(CVC), width=self.button_width, height=self.button_height)
            self.versus3_button.pack()
        self.versus4_button = tk.Button(self.window, text="单机模式", command=lambda: self.select_versus_mode(SP), width=self.button_width, height=self.button_height)
        self.versus4_button.pack()

    def select_versus_mode(self, versus_mode):
        self.versus1_button.pack_forget()
        if self.game_mode == GOMOKU:
            self.versus2_button.pack_forget()
            self.versus3_button.pack_forget()
        self.versus4_button.pack_forget()

        self.versus_mode = versus_mode
        if versus_mode == PVP:
            pass
        elif versus_mode == PVC:
            self.easy_button = tk.Button(self.window, text="简单难度", command=lambda: self.select_PVC_AI_Difficulty(EASY), width=self.button_width, height=self.button_height)
            self.easy_button.pack()
            self.medium_button = tk.Button(self.window, text="中等难度", command=lambda: self.select_PVC_AI_Difficulty(MEDIUM), width=self.button_width, height=self.button_height)
            self.medium_button.pack()
        elif versus_mode == CVC:
            self.window.title("请选择电脑1的难度！")
            self.easy_button = tk.Button(self.window, text="简单难度", command=lambda: self.select_CVC_AI1_Difficulty(EASY), width=self.button_width, height=self.button_height)
            self.easy_button.pack()
            self.medium_button = tk.Button(self.window, text="中等难度", command=lambda: self.select_CVC_AI1_Difficulty(MEDIUM), width=self.button_width, height=self.button_height)
            self.medium_button.pack()
        elif versus_mode == SP:
            self.choose_board_size()
    
    def select_CVC_AI1_Difficulty(self, difficulty):
        self.difficulty = difficulty
        self.easy_button.pack_forget()
        self.medium_button.pack_forget()

        self.window.title("请选择电脑2的难度！")
        self.easy_button = tk.Button(self.window, text="简单难度", command=lambda: self.select_CVC_AI2_Difficulty(EASY), width=self.button_width, height=self.button_height)
        self.easy_button.pack()
        self.medium_button = tk.Button(self.window, text="中等难度", command=lambda: self.select_CVC_AI2_Difficulty(MEDIUM), width=self.button_width, height=self.button_height)
        self.medium_button.pack()

    def select_CVC_AI2_Difficulty(self, difficulty):
        self.difficulty2 = difficulty
        self.easy_button.pack_forget()
        self.medium_button.pack_forget()

        self.window.title("请选择棋盘大小！")
        self.choose_board_size()

    def select_PVC_AI_Difficulty(self, difficulty):
        self.easy_button.pack_forget()
        self.medium_button.pack_forget()
        self.difficulty = difficulty
        self.choose_board_size()

    def choose_board_size(self):
        if self.game_mode == GOMOKU:
            self.button_8 = tk.Button(self.window, text="8路棋盘", command=lambda: self.select_board_size(8), width=self.button_width, height=self.button_height)
            self.button_8.pack()
            self.button_15 = tk.Button(self.window, text="15路棋盘", command=lambda: self.select_board_size(15), width=self.button_width, height=self.button_height)
            self.button_15.pack()
            self.button_19 = tk.Button(self.window, text="19路棋盘", command=lambda: self.select_board_size(19), width=self.button_width, height=self.button_height)
            self.button_19.pack()
        elif self.game_mode == GO:
            self.button_9 = tk.Button(self.window, text="9路棋盘", command=lambda: self.select_board_size(9), width=self.button_width, height=self.button_height)
            self.button_9.pack()
            self.button_13 = tk.Button(self.window, text="13路棋盘", command=lambda: self.select_board_size(13), width=self.button_width, height=self.button_height)
            self.button_13.pack()
            self.button_19 = tk.Button(self.window, text="19路棋盘", command=lambda: self.select_board_size(19), width=self.button_width, height=self.button_height)
            self.button_19.pack()
        elif self.game_mode == REVERSI:
            self.button_8 = tk.Button(self.window, text="8*8棋盘", command=lambda: self.select_board_size(9), width=self.button_width, height=self.button_height)
            self.button_8.pack()

    def select_board_size(self, size):
        self.board_size = size
        print("游戏模式：{}，对战模式：{}，棋盘大小：{}".format(self.game_mode, self.versus_mode, self.board_size))
        # 这里可以继续后续的游戏启动逻辑
        self.start_game()

    def start_game(self):
        self.window.destroy()
        if self.game_mode == GOMOKU:
            gomokuApp = GomokuApp(self.board_size, versus_mode=self.versus_mode, difficulty=self.difficulty, difficulty2=self.difficulty2)
            gomokuApp.game_gui.run()
        elif self.game_mode == GO:
            goApp = GoApp(self.board_size, versus_mode=self.versus_mode)
            goApp.game_gui.run()
        elif self.game_mode == REVERSI:
            reversiApp = ReversiApp(self.board_size, versus_mode=self.versus_mode)
            reversiApp.game_gui.run()

    # 加载存档
    def load_game(self):
        self.window.destroy()
        # 列出所有符合当前游戏模式的存档文件
        pattern = self.select_pattern()
        files = [f for f in os.listdir('.') if f.startswith(pattern) and f.endswith('.txt')]
        if not files:
            messagebox.showinfo("加载存档", "没有找到存档文件")
            return
        while True:
            # 让用户选择一个存档文件
            file = simpledialog.askstring("加载存档", "请选择存档文件：\n" + "\n".join(files))
            if file in files:
                print("加载存档：", file)
                break
            elif file == None:
                exit()
            else:
                messagebox.showinfo("加载存档", "存档文件不存在，请重新选择。")
        history_file = open(file, 'r')
        history_content = history_file.readlines()
        board_size = int(history_content[0])
        current_stone = history_content[1].strip()
        print("current player:", current_stone)
        board = [[None for _ in range(board_size)] for _ in range(board_size)]
        for i in range(2, len(history_content)):
            line = history_content[i]
            p, x, y = line.split(" ")
            x = int(x)
            y = int(y)
            board[x][y] = p
        if self.game_mode == GOMOKU:
            gomokuApp = GomokuApp(board_size, current_stone, board)
            gomokuApp.game_gui.run()
        elif self.game_mode == GO:
            goApp = GoApp(board_size, current_stone, board)
            goApp.game_gui.run()
        elif self.game_mode == REVERSI:
            reversiApp = ReversiApp(board_size, current_stone, board)
            reversiApp.game_gui.run()

    def select_pattern(self):
        if self.game_mode == GOMOKU:
            return 'gomoku_'
        elif self.game_mode == GO:
            return 'go_'
        elif self.game_mode == REVERSI:
            return "reversi_"

    def run(self):
        self.window.mainloop()

