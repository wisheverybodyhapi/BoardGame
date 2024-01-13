from GameGUI import *
import copy
from Config import *

class BoardGameApp:
    def __init__(self, board_size, current_player=BLACKPLAYER, history_board=None):
        self.game_gui = GameGUI(board_size)
        self.board_size = board_size
        self.game_type = None
        self.game_over = False
        self.game_mode = None
        self.can_undo = 0
        self.history_move = []
        self.current_player = current_player
        self.board = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]

        # 拷贝三份棋盘“快照”，悔棋和判断“打劫”时需要作参考
        self.last_3_board = copy.deepcopy(self.board)
        self.last_2_board = copy.deepcopy(self.board)
        self.last_1_board = copy.deepcopy(self.board)

        # 如果是加载存档，那么需要加载历史棋盘重新绘制
        if history_board != None:
            self.load_game(history_board)

        self.game_gui.create_buttons(self.give_up, self.undo_move, self.save_game, self.quit_game, self.judge_win, self.quit_move)
        # 绑定点击事件到画布    
        self.game_gui.canvas.bind("<Button-1>", self.place_piece)
    
    # 立刻认输button
    def give_up(self):
        if not self.game_over:
            loser = self.current_player
            winner = WHITEPLAYER if loser == BLACK else BLACKPLAYER
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
            self.game_gui.update_info(self.current_player + '要求悔棋一步')
            self.can_undo = 0

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
    def quit_move(self):
        pass
    
    # 退出游戏button
    def quit_game(self):
        exit()

    def switch_player(self):
        self.current_player = WHITE if self.current_player == BLACK else BLACK
        
    def load_game(self, board):
        self.board = board
        self.game_gui.redraw_board(board)


    def get_opponent(self):
        opponent = WHITE if self.current_player == BLACK else BLACK
        return opponent

    def update_board_snapshots(self):
        self.last_3_board = copy.deepcopy(self.last_2_board)
        self.last_2_board = copy.deepcopy(self.last_1_board)
        self.last_1_board = copy.deepcopy(self.board)

    def is_valid_move(self, row, column):
        if not self.game_over and self.board[row][column] is None:
            return True
        return False

    def place_piece(self, event):
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
