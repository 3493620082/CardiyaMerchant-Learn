# --coding=utf-8

"""
玩家对象
全局的使用使用模块级引入，这样能确保全局单例，然后只暴露getPlayer方法，隐藏对象和类
"""

import json

class Player:
    def __init__(self):
        pass

    def init_from_save_data(self, save_data: dict):
        """
        通过调用该方法设置角色属性
        :param save_data: 存档数据
        :return: 无
        """
        self.save_file_dir = save_data["save_file_dir"]
        self.player_name = save_data["base"]["player_name"]
        self.history_choices = save_data["base"]["history_choices"]
        self.is_show_tips = save_data["base"]["is_show_tips"]
        self.gender = save_data["character"]["gender"]
        self.age = save_data["character"]["age"]
        self.money = save_data["character"]["money"]
        self.lv = save_data["character"]["lv"]
        self.exp = save_data["character"]["exp"]
        self.attributes = save_data["character"]["attributes"]
        self.team_config = save_data["character"]["team_config"]
        self.carried_items = save_data["character"]["carried_items"]
        self.pack_weight = 0
        self.calculate_weight()  # 计算负重

    def save_to_save_file(self):
        """
        将数据保存到存档中
        因为base.json存档中的数据是不可变的基本信息，所以不用修改
        只需要修改character.json存档文件即可
        :return: 无
        """
        # ====================保存character.json====================
        with open(f"{self.save_file_dir}\\character.json", 'r', encoding="utf-8") as f:
            data = json.load(f)
        with open(f"{self.save_file_dir}\\character.json", 'w', encoding="utf-8") as f:
            data["age"] = self.age
            data["money"] = self.money
            data["lv"] = self.lv
            data["exp"] = self.exp
            data["attributes"] = self.attributes
            data["team_config"] = self.team_config
            data["carried_items"] = self.carried_items
            json.dump(data, f, ensure_ascii=False, indent=4)

    def tips_shown(self):
        """
        翻译：已显示提示界面
        修改base.json中的is_show_tips为False并保存
        :return: 无
        """
        with open(f"{self.save_file_dir}\\base.json", 'r', encoding="utf-8") as f:
            data = json.load(f)
        data["is_show_tips"] = False
        with open(f"{self.save_file_dir}\\base.json", 'w', encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def calculate_weight(self):
        # 计算背包中所有物品，总结负重
        self.pack_weight = 0
        for item in self.carried_items:
            self.pack_weight += item["item"]["weight"]

player = Player()

def getPlayer() -> Player:
    """
    返回玩家的全局实单例对象
    :return: 玩家对象 Player
    """
    return player

__all__ = ["getPlayer"]
