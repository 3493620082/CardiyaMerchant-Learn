import json
import random
from src.funcs import *

clear_screen()
change_color(Fore.GREEN)
print_top_title(GAME_NAME)
change_color(Fore.YELLOW)
# =======================标题分隔线=======================
# 界面
ui_lines = [
    "-"*100,
    " "*get_how_much_center_space("[春|226年|1月|上旬]")+"[春|226年|1月|上旬]"+" "*get_how_much_center_space("[春|226年|1月|上旬]"),
    "-"*100
]
citys = ["城市1", "城市23", "城市114514"]
for i in range(15):
    if random.choice([True, False]):
        city = random.choice(citys)
        max_space = 100-str_length(city)
        left_space = random.randint(0, max_space)
        ui_lines.append(
            " "*left_space+city+" "*(100-left_space-str_length(city))
        )
    else:
        ui_lines.append(" "*100)

ui_lines.append("-"*100)
ui_lines.append(
    "[人物|仓库|任务]"+" "*(100-str_length("[人物|仓库|任务][$1000|23.51/100kg|行动0/5]"))+"[$1000|23.51/100kg|行动0/5]"
)
ui_lines.append("-"*100)
for i in range(len(ui_lines)):
    if str_length(ui_lines[i]) != 100:
        ui_lines[i] += " "*(100-str_length(ui_lines[i]))
# 打印
for i in range(3):
    print(ui_lines[i])
change_color(Fore.CYAN)
for i in range(3, 18):
    print(ui_lines[i])
change_color(Fore.YELLOW)
for i in range(18, len(ui_lines)):
    print(ui_lines[i])
# =======================标题分隔线=======================
change_color(Fore.GREEN)
print_bottom_title(GAME_NAME)
#
# clear_screen()
#
# with open("src\\data\\citys.json", 'r', encoding="utf-8") as f:
#     data = json.load(f)
#     count = 0
#     for k, v in data["CITY"].items():
#         count += len(data["CITY"][k])
#     for k, v in data["TOWN"].items():
#         count += len(data["TOWN"][k])
#     for k, v in data["VILLAGE"].items():
#         count += len(data["VILLAGE"][k])
#     print(count)