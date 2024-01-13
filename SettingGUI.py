from GoApp import *
from GomokuApp import *

class SettingGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("请选择游戏模式：")
        self.width = 300
        self.height = 200
        self.button_width = 10
        self.button_height = 2
        self.game_mode = None
        self.game_type = None
        self.board_size = None
        self.window.geometry("{}x{}+0+0".format(self.width, self.height))

        # 游戏模式选择按钮
        self.button_gomoku = tk.Button(self.window, text=GOMOKU, command=lambda: self.select_game_mode(GOMOKU), width=self.button_width, height=self.button_height)
        self.button_gomoku.pack()

        self.button_go = tk.Button(self.window, text=GO, command=lambda: self.select_game_mode('围棋'), width=self.button_width, height=self.button_height)
        self.button_go.pack()

    def select_game_mode(self, game_mode):
        self.game_mode = game_mode
        self.button_gomoku.pack_forget()
        self.button_go.pack_forget()

        # 游戏类型选择按钮
        self.button_new_game = tk.Button(self.window, text="新游戏", command=lambda: self.select_game_type("新游戏"), width=self.button_width, height=self.button_height)
        self.button_new_game.pack()

        self.button_load_history = tk.Button(self.window, text="加载存档", command=lambda: self.select_game_type("加载存档"), width=self.button_width, height=self.button_height)
        self.button_load_history.pack()

    def select_game_type(self, game_type):
        self.game_type = game_type
        self.button_new_game.pack_forget()
        self.button_load_history.pack_forget()

        if self.game_type == "新游戏":
            self.choose_board_size()
        elif self.game_type == "加载存档":
            self.load_game()

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

    def select_board_size(self, size):
        self.board_size = size
        print("游戏模式：", self.game_mode, "，棋盘大小：", self.board_size)
        # 这里可以继续后续的游戏启动逻辑
        self.start_game()

    def start_game(self):
        self.window.destroy()
        if self.game_mode == GOMOKU:
            gomokuApp = GomokuApp(self.board_size)
            gomokuApp.game_gui.run()
        elif self.game_mode == GO:
            goApp = GoApp(self.board_size)
            goApp.game_gui.run()

    # 加载存档
    def load_game(self):
        self.window.destroy()
        # 列出所有符合当前游戏模式的存档文件
        pattern = "gomoku_" if self.game_mode == GOMOKU else "go_"
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
        current_player = history_content[1].strip()
        print("current player:", current_player)
        board = [[None for _ in range(board_size)] for _ in range(board_size)]
        for i in range(2, len(history_content)):
            line = history_content[i]
            p, x, y = line.split(" ")
            x = int(x)
            y = int(y)
            board[x][y] = p
        if self.game_mode == GOMOKU:
            gomokuApp = GomokuApp(board_size, current_player, board)
            gomokuApp.game_gui.run()
        elif self.game_mode == GO:
            goApp = GoApp(board_size, current_player, board)
            goApp.game_gui.run()

    def run(self):
        self.window.mainloop()

