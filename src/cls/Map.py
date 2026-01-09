# --coding=utf-8

"""
地图对象，用来控制地图在游戏内主界面的显示
"""

import os
import json
from src.const import *

class Map:
    def __init__(self):
        self.now_block_code = "1-1"
        self.row = 1
        self.col = 1
        self.now_towns = {}
        self.now_block = {}
        # 地图区块
        self.all_block = []
        for file_name in os.listdir("media\\block\\"):
            with open(f'media\\block\\{file_name}', 'r', encoding="utf-8") as f:
                self.all_block.append(json.load(f))
        # 为所有区块中的display中的城市拼接id
        self.add_id_for_city()
        # 更新display
        self.update_display()

    def add_id_for_city(self):
        # 为所有区块的display中的城市拼接id
        for i in range(len(self.all_block)):  # 遍历所有区块
            display = self.all_block[i]["display"]  # display是一个列表
            for j in range(len(display)):  # 遍历display
                line = display[j]  # 取出行
                if len(line) != 0:  # 行的长度不为0说明有城市存在
                    city = line.strip()  # 去除首位空格得到城市名
                    # 查找城市的id
                    for k in CITY_DATA.keys():
                        if CITY_DATA[k]["attr"]["name"] == city:
                            line += f'({k})'
                            break
                    # 更换display的行为修改后的行
                    self.all_block[i]["display"][j] = line
                # 这一级的循环因为需要查找所有行找城市所以不能在中途结束
            # 这一级的循环也是因为需要遍历所有区块所以不能中途结束

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
        for block in self.all_block:  # 遍历所有区块
            if block["block_code"] == self.now_block_code:  # 找到与当前区块坐标相等的区块
                self.now_block = block  # 取出当前区块
                self.now_towns.clear()  # 清空当前城市字典
                for town in self.now_block["towns"]:  # 遍历当前区块中的所有城市
                    for k, v in CITY_DATA.items():
                        if CITY_DATA[k]["attr"]["name"] == town:
                            self.now_towns[k] = town  # 添加键位id值为城市名的键值对到当前城市字典中
                            break
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

    def get_city_name_by_id(self, _id: str):
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