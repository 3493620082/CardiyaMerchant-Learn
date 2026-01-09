# --coding=utf-8

import os
import json

from colorama import Fore, Back, Style
from src.const import *
from datetime import datetime

def clear_screen():
    os.system("cls")

def str_length(s) -> int:
    """
    获取字符串长度的函数，中文字符处理为2，英文处理为1
    :param s: 要判断长度的字符串
    :return: 长度 int
    """
    length = 0
    s = str(s)
    for ch in s:
        if ord(ch) <= 127:
            length += 1
        else:
            length += 2
    return length

def center_space(s):
    return " "*((100 - str_length(s)) // 2)

def print_center_text(text, color=Fore.GREEN):
    print(color + " "*((100 - str_length(text)) // 2) + str(text) + Fore.GREEN)
def print_center_text_default_color(text):
    print(" "*((100 - str_length(text)) // 2) + str(text))

def show_ui(file_path, color=Fore.GREEN):
    """
    将ui文件打印出来
    :param color: 文本颜色，默认绿色
    :param file_path: 文件路径
    :return: 无
    """
    with open(file_path, 'r', encoding="utf-8") as f:
        print(color, end="")
        print(f.read())
        print(Fore.GREEN, end="")

def print_title(title):
    num = (100 - str_length(title)) // 2
    print()
    print("="*num + str(title) + "="*num)
    print()

def read_config():
    with open("config.json", 'r', encoding="utf-8") as f:
        return json.load(f)
def write_config(config_dict):
    with open("config.json", 'w', encoding="utf-8") as f:
        json.dump(config_dict, f, ensure_ascii=False, indent=4)

def show_honor():
    """
    打印成就界面
    :return: 无
    """
    with open("honor.json", 'r', encoding="utf-8") as f:
        data = json.load(f)["honor"]
        # data是一个列表
        for line in data:
            s = line[0]
            if line[1] == 0:  # 未达成
                space = " "*(100 - str_length(s) - str_length("[未达成]"))
                print(Fore.YELLOW + line[0] + space + Fore.RED + "[未达成]" + Fore.GREEN)
            else:  # 已达成
                space = " "*(100 - str_length(s) - str_length("[已达成]"))
                print(Fore.YELLOW + line[0] + space + Fore.GREEN + "[已达成]")

def load_save_files():
    """
    读取save文件夹下的所有存档文件并返回包含文件名的列表
    :return: 文件名列表
    """
    saves_list = []
    for name in os.listdir("save\\"):
        # 判断完整路径是否为目录
        if os.path.isdir(f"save\\{name}"):
            saves_list.append(f"save\\{name}")
    return saves_list

def space(length: int):
    return " "*length

def show_save_files():
    """
    打印存档列表
    :return: 无
    """
    print(Fore.YELLOW, end="")
    saves_list = load_save_files()
    for i in range(len(saves_list)):
        line = f"{FIVE_SPACE}{i+1}. " + saves_list[i].replace("save\\", "") + "\n"
        print(line)
    print(Fore.GREEN, end="")

def load_save_data(save_file_dir):
    """
    读取存档的数据
    :param save_file_dir: 存档文件夹的路径
    :return: 存档数据组成的字典 dict[数据文件: 数据]
    """
    data = {"save_file_dir": save_file_dir}
    # ====================读取base.json====================
    with open(f"{save_file_dir}\\base.json", 'r', encoding="utf-8") as f:
        data["base"] = json.load(f)
    # ====================读取character.json====================
    with open(f"{save_file_dir}\\character.json", 'r', encoding="utf-8") as f:
        data["character"] = json.load(f)
    # ====================读取state.json====================
    with open(f"{save_file_dir}\\state.json", 'r', encoding="utf-8") as f:
        data["state"] = json.load(f)

    # 返回
    return data

def check_str_has_char(s, chars):
    """
    判断字符串中是否存在指定字符，存在返回True否则返回False
    :param s: 要判断的字符串
    :param chars: 字符组成的集合
    :return: 布尔值
    """
    for c in s:
        if c in chars:
            return True
    return False

def change_color(color):
    print(color, end="")

def get_item_data_by_id(id: int) -> dict:
    """
    返回物品数据通过id识别
    :param id: 物品id
    :return: 物品数据 dict
    """
    for item in GAME_ITEMS_DATABASE:
        if item["item_id"] == id:
            return item
    return {"item_id": -1, "item_name": "该物品不存在", "price": 0}
def get_item_data_by_name(name: str) -> dict:
    """
    返回物品数据通过物品名
    :param name: 物品名
    :return: 物品数据 dict
    """
    for item in GAME_ITEMS_DATABASE:
        if item["item_name"] == name:
            return item
    return {"item_id": -1, "item_name": "该物品不存在", "price": 0}

def create_save_files(player_name: str, history_choices: dict[str, str], begin_money: int,
                      attributes: dict[str, int], team_config: dict[str, int], carried_items: list) -> list:
    """
    创建游戏存档并写入玩家数据
    :param player_name: 玩家名
    :param history_choices: 经历
    :param begin_money: 启动资金
    :param attributes: 属性
    :param team_config: 团队配置
    :param carried_items: 物品
    :return: True和存档文件夹;False和None
    """
    # 获取当前时间
    create_datetime = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    # 将玩家名和当前时间拼接为存档名
    save_file_dir = f"save\\{player_name} {create_datetime}"
    # 创建存档文件夹
    try:
        os.mkdir(save_file_dir)
    except Exception:
        return False
    # 将不同的数据写入到不同的文件
    try:
        # =======================base.json=======================
        with open(f"{save_file_dir}\\base.json", 'w', encoding="utf-8") as f:
            base_json = {
                "create_datetime": create_datetime,
                "player_name": player_name,
                "history_choices": history_choices,
                "is_show_tips": True
            }
            json.dump(base_json, f, ensure_ascii=False, indent=4)
        # =======================character.json=======================
        with open(f"{save_file_dir}\\character.json", 'w', encoding="utf-8") as f:
            character_json = {
                "gender": history_choices["gender"],
                "age": 18,
                "money": begin_money,
                "lv": 1,
                "exp": 0,
                "attributes": attributes,
                "team_config": team_config,
                "carried_items": carried_items
            }
            json.dump(character_json, f, ensure_ascii=False, indent=4)
        # =======================state.json=======================
        with open(f"{save_file_dir}\\state.json", 'w', encoding="utf-8") as f:
            state_json = {
                "date": {
                    "year": 100,
                    "month": 1,
                    "day": 1
                },
                "stay_city": history_choices["city"],
                "action_point": 5,
                "mapped": []
            }
            for k in CITY_DATA.keys():
                if CITY_DATA[k]["attr"]["name"] == history_choices["city"]:
                    _id = k
                    break
            state_json["mapped"].append(
                {
                    "id": _id,
                    "city": history_choices["city"]
                }
            )
            json.dump(state_json, f, ensure_ascii=False, indent=4)
        # =======================honor.json=======================
        with open("src\\data\\honor_temp.json", 'r', encoding="utf-8") as f:  # 读取模板文件中的数据
            honor_json = json.load(f)
        with open(f"{save_file_dir}\\honor.json", 'w', encoding="utf-8") as f:  # 写入
            json.dump(honor_json, f)

        # 返回True代表成功
        return [True, save_file_dir]
    except Exception:
        return [False, None]

def get_how_much_center_space(text: str) -> int:
    """
    返回居中所需的空格的数量，可以拿这个数去显示其他的字符
    :param text: 文本
    :return: 空格数量
    """
    return (100 - str_length(text)) // 2

def print_top_title(title: str):
    num = (100 - str_length(title)) // 2
    print()
    print("=" * num + str(title) + "=" * num)
def print_bottom_title(title: str):
    num = (100 - str_length(title)) // 2
    print("="*num + str(title) + "="*num)
    print()
