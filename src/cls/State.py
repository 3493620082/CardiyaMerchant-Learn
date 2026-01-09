# --coding=utf-8

"""
State类
用来保存当前游戏运行时的一些状态数据
例如日期，所在城市，行动力点数等
"""

import json

class State:
    def __init__(self):
        pass

    def init_from_save_data(self, save_data: dict):
        """
        调用该方法从存档中初始化状态数据
        :param save_data: 存档数据
        :return: 无
        """
        self.save_file_dir = save_data["save_file_dir"]
        self.date = save_data["state"]["date"]
        self.stay_city = save_data["state"]["stay_city"]
        self.action_point = save_data["state"]["action_point"]
        self.mapped = save_data["state"]["mapped"]

    def save_to_save_file(self):
        """
        将数据保存到state.json存档文件中
        :return: 无
        """
        with open(f"{self.save_file_dir}\\state.json", 'r', encoding="utf-8") as f:
            data = json.load(f)
        with open(f"{self.save_file_dir}\\state.json", 'w', encoding="utf-8") as f:
            data["date"] = self.date
            data["stay_city"] = self.stay_city
            data["action_point"] = self.action_point
            data["mapped"] = self.mapped
            json.dump(data, f, ensure_ascii=False, indent=4)

state = State()

def getState() -> State:
    """
    返回状态对象
    :return: 状态对象state
    """
    return state

__all__ = ["getState"]
