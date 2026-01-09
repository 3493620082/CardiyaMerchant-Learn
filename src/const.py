# --coding=utf-8

"""游戏常量"""

import json

GAME_NAME = "卡迪亚行商"
FIVE_SPACE = " "*5

# 游戏设置
with open("config.json", 'r', encoding="utf-8") as f:
    CONFIG = json.load(f)

# 所有城市
with open("src\\data\\citys.json", 'r', encoding="utf-8") as f:
    CITYS = json.load(f)

# 所有城市的详细属性
with open("src\\data\\city_data.json", 'r', encoding="utf-8") as f:
    CITY_DATA = json.load(f)

# 玩家名禁止出现的字符
PLAYER_NAME_ERROR_CHARS = ('~','`','!','@','#','$','%','^','&','*','(',')','=','+','/','.',',','<','>','?',':',';','{','}','[',']','\\','|',
                           '，','。','《','》','、','？','；','：','‘','“','”','【','】','—','）','（','…','￥','！','~')

# 创建新游戏时选择的出生城市，这里只使用城市，不使用乡镇和村庄
NEW_PLAYER_CITYS = CITYS["CITY"]

# 创建新游戏时展示玩家信息的页面的属性列表
with open("src\\data\\attribute.json", 'r', encoding="utf-8") as f:
    PLAYER_ATTRIBUTES = json.load(f)["attributes"]

# 创建新游戏时展示玩家信息页面右边的经历列表
with open("src\\data\\choice_bonus.json", 'r', encoding="utf-8") as f:
    CHOICE_BONUS = json.load(f)

# 物品数据库
with open("src\\data\\items.json", 'r', encoding="utf-8") as f:
    GAME_ITEMS_DATABASE = json.load(f)["items"]

