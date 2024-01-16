from UserAccount import *

class HumanPlayer:
    def __init__(self, current_game, name='游客', user_account=None):
        self.user_account = user_account
        self.name = name if user_account == None else user_account.username
        self.ip_address = None
        self.port = None
        self.record = {'wins': 0, 'losses': 0}
        self.status = 'offline'
        self.current_game = current_game
        self.last_login_time = None
        self.current_game.game_gui.canvas.bind("<Button-1>", self.make_move)

    def login(self, username, password, account_manager):
        # 用户登录
        if account_manager.login(username, password):
            self.user_account = account_manager.accounts[username]
            self.name = username
            return True
        return False

    def register(self, username, password, account_manager):
        # 用户注册
        return account_manager.register(username, password)

    def update_record(self, win):
        # 更新用户战绩
        if self.user_account:
            self.user_account.update_record(win)


    def make_move(self, event):
        row, column = self.current_game.get_click_position(event)
        current_stone = self.current_game.current_stone
        current_player = self.current_game.current_player.name
        print("current_player", current_player)
        self.current_game.place_piece(row, column, current_player, current_stone)

    def connect(self, ip_address, port):
        # 实现玩家的网络连接逻辑
        pass

    def send_message(self, message):
        # 实现发送消息的逻辑
        pass

    def receive_message(self):
        # 实现接收消息的逻辑
        pass

