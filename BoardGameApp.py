from GameGUI import *
import copy

class BoardGameApp:
    def __init__(self, board_size, current_player='Black', history_board=None):
        self.game_gui = GameGUI(board_size)
        self.board_size = board_size
        self.game_type = None
        self.game_over = False
        self.can_undo = 0
        self.history_move = []
        self.current_player = current_player
        self.board = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.board = history_board if history_board else self.board
        # 拷贝三份棋盘“快照”，悔棋和判断“打劫”时需要作参考
        self.last_3_board = copy.deepcopy(self.board)
        self.last_2_board = copy.deepcopy(self.board)
        self.last_1_board = copy.deepcopy(self.board)
        if history_board:
            self.load_game()
        self.game_gui.create_buttons(self.give_up, self.undo_move, self.save_game, self.quit_game, self.judge_win, self.quit_exec)
        # 绑定点击事件到画布    
        self.game_gui.canvas.bind("<Button-1>", self.place_piece)
    
    # 立刻认输button
    def give_up(self):
        if not self.game_over:
            loser = self.current_player
            winner = "White" if loser == "Black" else "Black"
            messagebox.showinfo("游戏结束", f"{loser} 认输了，{winner} 赢了！")
            self.game_gui.update_info(f"{loser} 认输了。")
            self.game_over = True

    # 悔棋button
    def undo_move(self):
        if self.can_undo == 2 and not self.game_over:
            self.board = self.last_3_board
            self.update_board_snapshots()
            self.game_gui.clear_board()
            self.game_gui.redraw_board(self.board)
            self.game_gui.update_info('悔棋一步')
            self.can_undo = 0

    # 保存游戏button
    def save_game(self):
        if self.game_over:
            messagebox.showinfo("提示", "游戏已结束，无需保存。")
            return
        # 列出所有符合当前游戏模式的存档文件
        pattern = "gomoku_" if self.game_mode == "五子棋" else "go_"
        files = [f for f in os.listdir('.') if f.startswith(pattern) and f.endswith('.txt')]
        save_file = "{}_save_{}.txt".format(self.game_mode, len(files))
        with open(save_file, "w") as file:
            file.write(str(self.board_size) + "\n")
            file.write(self.current_player + "\n")
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
    def quit_exec(self):
        pass
    
    # 退出游戏button
    def quit_game(self):
        exit()

    def switch_player(self):
        self.current_player = "White" if self.current_player == "Black" else "Black"
        
    def load_game(self):
        print("redraw chess board ~~~~~~~~")
        self.game_gui.redraw_board(self.board)


    def update_board_snapshots(self):
        self.last_3_board = copy.deepcopy(self.last_2_board)
        self.last_2_board = copy.deepcopy(self.last_1_board)
        self.last_1_board = copy.deepcopy(self.board)


    def place_piece(self, event):
        # 落子规则需具体实现
        pass

    def check_win(self, x, y):
        # 检查胜利条件
        pass
    
    # 用于悔棋后，进行的棋盘状态恢复
    def restore_game():
        pass
