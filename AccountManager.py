from UserAccount import *

class AccountManager:
    def __init__(self, filepath='accounts.json'):
        self.filepath = filepath
        self.accounts = self.load_accounts()

    def load_accounts(self):
        # 从文件加载用户信息
        try:
            with open(self.filepath, 'r') as file:
                return {data['username']: UserAccount(**data, hashed=True) for data in json.load(file)}
        except FileNotFoundError:
            return {}

    def save_accounts(self):
        # 保存用户信息到文件
        with open(self.filepath, 'w') as file:
            for account in self.accounts.values():
                print(account.to_dict())
            json.dump([account.to_dict() for account in self.accounts.values()], file)

    def register(self, username, password):
        # 注册新用户
        if username in self.accounts:
            return False
        self.accounts[username] = UserAccount(username, password)  # 直接传入原始密码
        self.save_accounts()
        return True

    def update_record(self, player, win):
        # 更新战绩
        if win:
            self.accounts[player].wins += 1
        else:
            self.accounts[player].losses += 1

    def login(self, username, password):
        # 登录验证
        user = self.accounts.get(username)

        if user and user.verify_password(password):
            return True
        else:
            return False
