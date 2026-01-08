# --coding=utf-8

"""
地图对象，用来控制地图在游戏内主界面的显示
"""

import os
import json

class Map:
    def __init__(self):
        self.now_block_code = "1-1"
        self.now_towns = {}
        self.row = 1
        self.col = 1
        self.now_block = {}
        # 地图区块
        self.all_block = []
        for file_name in os.listdir("media\\block\\"):
            with open(f'media\\block\\{file_name}', 'r', encoding="utf-8") as f:
                self.all_block.append(json.load(f))
        # 城市数据
        with open("src\\data\\city_data.json", 'r', encoding="utf-8") as f:
            self.city_data = json.load(f)
        # 为所有城市添加id
        for i in range(len(self.all_block)):
            display = self.all_block[i]["display"]
            for j in range(len(display)):
                line = display[j]
                if len(line.strip()) != 0:
                    city_name = line.strip()
                    id_str = f'({self.city_data[city_name]["id"]})'
                    line += id_str
                display[j] = line
            self.all_block[i]["display"] = display
        # 更新display
        self.update_display()

    def init_player_location(self, stay_city: str):
        """
        根据玩家当前所在的城市来跳转到该城市所在的区块
        :param stay_city: 城市名
        :return: 无
        """
        for block in self.all_block:
            if stay_city in block["towns"]:
                self.now_block_code = block["block_code"]
                self.row = block["grid_position"]["row"]
                self.col = block["grid_position"]["col"]
                self.update_display()
                break

    def update_display(self):
        """
        修改显示内容
        :return: 无
        """
        for block in self.all_block:
            if block["block_code"] == self.now_block_code:
                self.now_block = block
                # 遍历当前区块中的城市
                self.now_towns.clear()
                for town in self.now_block["towns"]:
                    _id = str(self.city_data[town]["id"])
                    self.now_towns[_id] = town
                # 更新显示
                self.display = block["display"]
                break

    def move(self, key):
        """
        根据输入的值判断上下左右移动
        :param key: 键盘值
        :return: 无
        """
        if key == "W" or key == "w":  # 上移
            if self.row != 1:
                self.row -= 1
        elif key == "S" or key == "s":  # 下移
            if self.row != 5:
                self.row += 1
        elif key == "A" or key == "a":  # 左移
            if self.col != 1:
                self.col -= 1
        elif key == "D" or key == "d":  # 右移
            if self.col != 5:
                self.col += 1
        # 修改now_block_code的值
        self.now_block_code = f"{self.row}-{self.col}"
        # 更新地图
        self.update_display()

    def get_city_name_from_id(self, _id: str):
        """
        返回城市名
        :param _id: 城市id
        :return: 城市名
        """
        return self.now_towns[_id]

_map = Map()

def getMap() -> Map:
    """
    返回地图对象
    :return: Map地图对象
    """
    return _map

__all__ = ["getMap"]