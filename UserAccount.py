import json
import hashlib

class UserAccount:
    def __init__(self, username, password, wins=0, losses=0, hashed=False):
        self.username = username
        self.password = password if hashed else self.hash_password(password)
        self.wins = wins
        self.losses = losses

    def hash_password(self, password):
        # 密码加密
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password):
        # 验证密码
        print("self.hash_password", self.hash_password(password))
        print("self.password", self.password)
        print(self.hash_password(password))
        return self.hash_password(password) == self.password

    def to_dict(self):
        # 转换为字典，便于存储
        return {
            "username": self.username,
            "password": self.password,
            "wins": self.wins,
            "losses": self.losses
        }
