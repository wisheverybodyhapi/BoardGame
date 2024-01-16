import tkinter as tk
import time
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import *
from PIL import Image, ImageTk
import os
import time
from Config import *

class GameGUI:
    def __init__(self, current_game):
        self.current_game = current_game
        self.board_size = current_game.board_size
        self.cell_size = 35  # 设置每个格子的大小
        self.background_image_path = "chessboard.png"
        self.canvas_size = self.cell_size * self.board_size
        self.width=self.canvas_size + self.cell_size
        self.height=self.canvas_size + self.cell_size
        self.window = tk.Tk()
        self.window.title("棋盘")
        self.canvas = tk.Canvas(self.window, width=self.width, height=self.height, bg='white')
        self.canvas.pack()
        self.load_background_image()
        self.draw_board()
        # 设置窗口位置为左上角
        self.window.geometry("{}x{}+0+0".format(self.width, self.height))  # 宽度x高度+横向偏移+纵向偏移
        self.info_window, self.info_text = self.create_info_window()

    def load_background_image(self):
        try:
            original_image = Image.open(self.background_image_path)
            resized_image = original_image.resize((self.canvas_size + self.cell_size, self.canvas_size + self.cell_size))
            self.background_image = ImageTk.PhotoImage(resized_image)
            self.background_image_id = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)
        except IOError:
            print("图像文件加载失败")

    def draw_board(self):
        for i in range(self.canvas_size):
            # 绘制横线，确保只绘制所需数量的线条
            self.canvas.create_line(self.cell_size, (i + 1) * self.cell_size,
                                    self.canvas_size, (i + 1) * self.cell_size)
            # time.sleep(0.5)
            # 绘制竖线，同样确保只绘制所需数量的线条
            self.canvas.create_line((i + 1) * self.cell_size, self.cell_size,
                                    (i + 1) * self.cell_size, self.canvas_size)
            # time.sleep(0.5)

    def create_info_window(self):
        info_window = tk.Toplevel(self.window)
        info_window.title("游戏互动窗口")
        # 设置互动窗口位置为左上角
        info_window.geometry("300x500+{}+0".format(self.width))  # 宽度x高度+横向偏移+纵向偏移
        info_text = tk.Text(info_window, height=20, width=35)
        info_text.pack()
        return info_window, info_text

    def clear_board(self):
        # 清空棋盘并重新绘制背景和棋盘
        self.canvas.delete("all")
        self.load_background_image()
        self.draw_board()
    
    def redraw_board(self, board):
        self.clear_board()
        # 重新绘制棋盘上的所有棋子
        for row in range(len(board)):
            for col in range(len(board)):
                player = board[row][col]
                if player is not None:
                    draw_color = BLACK if player ==  BLACK else WHITE
                    x = (col + 1) * self.cell_size
                    y = (row + 1) * self.cell_size
                    self.canvas.create_oval(x - self.cell_size // 4, y - self.cell_size // 4,
                                                     x + self.cell_size // 4, y + self.cell_size // 4,
                                                     fill=draw_color)

    def create_buttons(self, give_up_callback, undo_move_callback, save_game_callback, quit_game_callback,
                    judge_win_callback, quit_exec_callback):
        current_player = self.current_game.current_player
        current_stone = self.current_game.current_stone
        opponent_stone = self.current_game.get_opponent(current_stone)
        
        give_up_button = tk.Button(self.info_window, text="立刻认输", command=lambda: give_up_callback(current_player, current_stone, opponent_stone))
        give_up_button.pack()

        undo_button = tk.Button(self.info_window, text="悔棋一步", command=lambda: undo_move_callback(current_player, current_stone))
        undo_button.pack()

        save_button = tk.Button(self.info_window, text="保存游戏", command=save_game_callback)
        save_button.pack()

        judge_win = tk.Button(self.info_window, text="判断胜负", command=judge_win_callback)
        judge_win.pack()
        
        quit_exec = tk.Button(self.info_window, text="放弃此步", command=lambda: quit_exec_callback(current_player, current_stone))
        quit_exec.pack()

        quit_button = tk.Button(self.info_window, text="退出游戏", command=quit_game_callback)
        quit_button.pack()


    def update_info(self, text):
        self.info_text.insert(tk.END, text + "\n")
        self.info_text.see(tk.END)  # 自动滚动到最新信息

    def run(self):
        self.window.mainloop()
