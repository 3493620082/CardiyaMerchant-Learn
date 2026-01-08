import time

from src.funcs import *
from src.const import *
from src.cls.Player import getPlayer
from src.cls.State import getState
from src.cls.Map import getMap

# 退出页
def gamePage_quit():
    """
    退出页，显示一些选项
    1. 返回主菜单
    2. 游戏设置
    3. 存档成就
    4. 继续游戏
    :return: 根据不同结果返回不同的值
    """
    while True:
        clear_screen()
        print_title(GAME_NAME)
        change_color(Fore.YELLOW)
        print_center_text_default_color("1. 返回主菜单\n")
        print_center_text_default_color("2. 游戏设置\n")
        print_center_text_default_color("3. 存档成就\n")
        print_center_text_default_color("4. 继续游戏")
        change_color(Fore.GREEN)
        print_title(GAME_NAME)
        choice = input(center_space("选择:") + "选择:")
        if choice == "1":
            return "quit"
        elif choice == "2":
            pass
        elif choice == "3":
            pass
        elif choice == "4":
            return None

# 将玩家选择的经历处理为人物属性
def handle_choices_to_attribute(choices: dict[str, str]) -> dict[str, int]:
    """
    处理玩家的选择，并将其转化为具体的属性等级
    :param choices: 玩家的选择组成的字典
    :return: 技能等级的字典
    """
    player_attributes = {"打探":0,"学识":0,"魅力":0,"鉴定":0,"人脉":0,"辎重":0,"贷款":0}
    # "没落贵族后裔", "城邦富商之家", "自由民工匠之子", "农奴之子"
    if choices["family"] == "没落贵族后裔":
        player_attributes["学识"] += 1
    elif choices["family"] == "城邦富商之家":
        player_attributes["学识"] += 1
    elif choices["family"] == "自由民工匠之子":
        player_attributes["鉴定"] += 1
    elif choices["family"] == "农奴之子":
        player_attributes["辎重"] += 1
    # "父亲:退役骑士队长 母亲:贵族妇人", "父亲:商队统领 母亲:货物交易员", "父亲:铁匠 母亲:木匠", "父亲:农奴 母亲:纺织工"
    if choices["parent"] == "父亲:退役骑士队长 母亲:贵族妇人":
        player_attributes["人脉"] += 1
    elif choices["parent"] == "父亲:商队统领 母亲:货物交易员":
        player_attributes["鉴定"] += 1
    elif choices["parent"] == "父亲:铁匠 母亲:木匠":
        player_attributes["鉴定"] += 1
    elif choices["parent"] == "父亲:农奴 母亲:纺织工":
        player_attributes["辎重"] += 1
    # "无忧无虑的贵族公子，童年快乐且丰富", "童年在商队的马车上度过", "在父亲的铁匠铺当学徒", "在田野中奔跑，试着与大自然共处"
    if choices["child"] == "无忧无虑的贵族公子，童年快乐且丰富":
        player_attributes["学识"] += 1
    elif choices["child"] == "童年在商队的马车上度过":
        player_attributes["打探"] += 1
    elif choices["child"] == "在父亲的铁匠铺当学徒":
        player_attributes["鉴定"] += 1
    elif choices["child"] == "在田野中奔跑，试着与大自然共处":
        player_attributes["魅力"] += 1
    # "皇家官方行商", "宝物收藏家", "大陆旅行者", "技艺精湛的工匠"
    if choices["dream"] == "皇家官方行商":
        player_attributes["打探"] += 1
    elif choices["dream"] == "宝物收藏家":
        player_attributes["鉴定"] += 1
    elif choices["dream"] == "大陆旅行者":
        player_attributes["人脉"] += 1
    elif choices["dream"] == "技艺精湛的工匠":
        player_attributes["鉴定"] += 1
    return player_attributes

# 根据玩家选择的经历初始化资金、团队配置和初始物资
def init_beginMoney_teamConfig_carriedItems(choices: dict[str, str]) -> list:
    """
    根据玩家的家族选择，配置启动资金、团队配置和初始货物
    :param choices: 玩家的选择组成的字典
    :return: [启动资金, 团队配置, 初始货物]
    """
    # return要返回的列表
    result = [0, {"packhorse": 0, "weight": 0}, []]
    # 家族
    if choices["family"] == "没落贵族后裔":
        result[0] = 50
        result[1]["packhorse"] = 2
        item = get_item_data_by_name("黄金项链")
        result[2].append({"item": item, "quantity": 1})
    if choices["family"] == "城邦富商之家":
        result[0] = 50
        result[1]["packhorse"] = 3
        item = get_item_data_by_name("维特鲁姆玉佩")
        result[2].append({"item": item, "quantity": 1})
    elif choices["family"] == "自由民工匠之子":
        result[0] = 20
        result[1]["packhorse"] = 1
        item = get_item_data_by_name("铁十字剑")
        result[2].append({"item": item, "quantity": 1})
    elif choices["family"] == "农奴之子":
        result[0] = 1
        item = get_item_data_by_name("布衣")
        result[2].append({"item": item, "quantity": 1})
    # 计算负重(单位kg)
    result[1]["weight"] = result[1]["packhorse"] * 50
    # 返回结果
    return result

# 播放背景故事
def show_background_story():
    """
    展示背景故事
    :return: 无
    """
    # 读取文件
    with open("media\\text\\background_story.txt", 'r', encoding="utf-8") as f:
        content = f.read()
    content = content.split("\n")
    for line in content:
        clear_screen()
        print_title("卡迪亚行商")
        print(Fore.YELLOW, end="")
        if len(line) > 45:
            for i in range(0, len(line), 45):
                print(" "*5 + line[i:i+45])
            print(Fore.GREEN, end="")
        else:
            print(" "*5 + line + Fore.GREEN)
        input(center_space("任意键继续...") + "任意键继续...")

# 创建新游戏的页面
def gamePage_new_game():
    """
    选择：家族、父母、童年、目标、城市、性别
    输入：玩家名
    初始化：属性
    :return: 成功的话返回一个列表[True, 存档名]
    """
    # 定义一个子函数处理选择的过程
    def sub_func(options, title):
        """
        处理选择的过程
        :param title: 提示文本，例如：你的家族是，你父母的职业是...
        :param options: 要选择的元素组成的元组
        :return: 选择出来的元素
        """
        while True:
            clear_screen()
            print_title("卡迪亚行商")
            print_center_text(title, Fore.YELLOW)
            print(Fore.YELLOW)
            for i in range(len(options)):
                print(" " * 5 + f"{i + 1}. {options[i]}")
            print(Fore.GREEN, end="")
            print_title("卡迪亚行商")
            try:
                choice = int(input(center_space("选择: ") + "选择: "))
                if choice in [1, 2, 3, 4]:
                    return options[choice - 1]
                else:
                    print("选项不存在!")
                    time.sleep(2)
            except Exception:
                print("输入有误!")
                time.sleep(2)
    # 这里添加循环是因为最后选择完所有选项后仍可以重新选择
    flag = True
    while flag:
        # 玩家的选择
        choices = {"family": "", "parent": "", "child": "", "dream": "", "player_name": "", "city": "", "gender": ""}
        # 家族
        familys = ("没落贵族后裔", "城邦富商之家", "自由民工匠之子", "农奴之子")
        choices["family"] = sub_func(familys, "你的家族是")
        # 父母职业
        parents = ("父亲:退役骑士队长 母亲:贵族妇人", "父亲:商队统领 母亲:货物交易员", "父亲:铁匠 母亲:木匠", "父亲:农奴 母亲:纺织工")
        choices["parent"] = sub_func(parents, "你父母的职业是")
        # 童年
        childs = ("无忧无虑的贵族公子，童年快乐且丰富", "童年在商队的马车上度过", "在父亲的铁匠铺当学徒", "在田野中奔跑，试着与大自然共处")
        choices["child"] = sub_func(childs, "你的童年是")
        # 梦想
        dreams = ("皇家官方行商", "宝物收藏家", "大陆旅行者", "技艺精湛的工匠")
        choices["dream"] = sub_func(dreams, "你的梦想是")
        # 城市
        city_ready = {"country": "", "city": ""}
        # 选择国家和城市
        while True:
            clear_screen()
            print_title(GAME_NAME)
            change_color(Fore.YELLOW)
            print_center_text_default_color("你所属的国家是")
            print()  # 换行增加美感
            countrys = list(NEW_PLAYER_CITYS.keys())
            for i in range(len(countrys)):
                print(" "*5 + f"{i+1}. {countrys[i]}")
            change_color(Fore.GREEN)
            print_title(GAME_NAME)
            try:
                choice = int(input(center_space("选择: ") + "选择: ")) - 1
                if choice < 0:  # 如果输入的索引小于0主动抛出错误
                    raise Exception()
                country = countrys[choice]  # 获取选中的国家，如果索引不在范围内直接抛出异常然后被处理
                city_ready["country"] = country
                # 选择具体城市
                while True:
                    clear_screen()
                    print_title(GAME_NAME)
                    change_color(Fore.YELLOW)
                    print_center_text_default_color("你现在的城市是")
                    print()
                    for i in range(len(NEW_PLAYER_CITYS[country])):  # 遍历所属国家的城市列表
                        print(" "*5 + f"{i+1}. {NEW_PLAYER_CITYS[country][i]}")
                    change_color(Fore.GREEN)
                    print_title(GAME_NAME)
                    try:
                        choice_city = int(input(center_space("选择: ") + "选择: "))
                        if choice_city == -1:  # 选择-1就退出重新选国家
                            break
                        """
                        如果能执行到这里说明输入的值不是-1，
                        然后判断如果>=1且<=列表的长度说明索引是合法的，
                        因为用户输入的是编号不是索引，所以判断的范围是1-列表长度，
                        就可以放心进行下一步了
                        """
                        if 1 <= choice_city <= len(NEW_PLAYER_CITYS[country]):
                            city_ready["city"] = NEW_PLAYER_CITYS[country][choice_city-1]
                            break
                        else:
                            raise Exception()
                    except Exception:
                        print("输入有误!")
                        time.sleep(2)
                # 城市输入的循环结束后判断city_ready中的值，如果都不为空说明是选好了，如果city为空说明要重新选择国家
                if city_ready["country"] and city_ready["city"]:
                    choices["city"] = city_ready["city"]
                    break
            except Exception:
                print("输入有误!")
                time.sleep(10)
        # 性别
        while True:
            clear_screen()
            print_title(GAME_NAME)
            change_color(Fore.YELLOW)
            print_center_text_default_color("你的性别是")
            print()
            print_center_text_default_color("1. 先生")
            print_center_text_default_color("2. 女士")
            change_color(Fore.GREEN)
            print_title(GAME_NAME)
            choice = input(center_space("选择: ") + "选择: ")
            if choice == "1":
                choices["gender"] = "先生"
                break
            elif choice == "2":
                choices["gender"] = "女士"
                break
        # 名字
        while True:
            clear_screen()
            print_title("卡迪亚行商")
            change_color(Fore.YELLOW)
            print("\n\n\n")
            if choices["gender"] == "先生":
                print_center_text_default_color("伟大的先生, 你的名字是")
            elif choices["gender"] == "女士":
                print_center_text_default_color("尊贵的女士, 你的名字是")
            print("\n\n\n")
            change_color(Fore.GREEN)
            print_title("卡迪亚行商")
            player_name = input(center_space("输入: ") + "输入: ")
            if player_name and (not check_str_has_char(player_name, PLAYER_NAME_ERROR_CHARS)):  # 用户名存在且没有违规字符
                if len(player_name) > 30:
                    print("长度太长!请重新输入!")
                    time.sleep(2)
                else:
                    choices["player_name"] = player_name
                    break
            else:
                print("输入的名字中含有违规字符!")
                time.sleep(2)
        # 处理所有选项
        """
        先根据不同的选择初始化角色属性
        然后在界面中显示各种信息，属性等级，玩家名，初始金币等
        """
        while True:
            clear_screen()
            print_title("你的信息")
            change_color(Fore.YELLOW)
            print_center_text_default_color(f"{choices["player_name"]}{choices["gender"]}")
            print()
            # 让属性和经历两个列表分别占一半，左右显示，计算空格：(50-属性)//2，(50-经历)//2
            space = " "*((50 - 4)//2)
            print(f"{space}属性{space}{space}经历{space}\n")
            """
            因为属性和经历要在同一行显示，所以需要在同一行打印
            先打印[5空格]属性及等级，因为开头和结尾都有5个空格的间隔，所以实际可使用宽度是90字符
            左边分配45，右边也是45，如果右边超长的话就换行，然后仍然从中间开始输出
            举例：
            12345属性1[*][ ][ ][ ][ ]                         家族:具体的选项以及属性加成说明
            """
            # 玩家属性及等级
            player_attributes = handle_choices_to_attribute(choices)
            # 经历选项及属性加成说明CHOICE_BONUS
            count = 1
            # 打印玩家属性和经历
            change_color(Fore.CYAN)
            for k, v in player_attributes.items():
                # lv属性等级
                lv = "[*]"*v + "[ ]"*(5-v)
                # 左
                left = f"{k} {lv}"
                left_end = " "*(45 - str_length(left))
                left += left_end
                # 右
                space_a = " "*55
                if count == 1:
                    add = CHOICE_BONUS["family"][choices["family"]]
                    right = f"家族:{choices["family"]}\n{space_a}[{add}]"
                elif count == 2:
                    add = CHOICE_BONUS["parent"][choices["parent"]]
                    right = f"父母:{choices["parent"]}\n{space_a}[{add}]"
                elif count == 3:
                    add = CHOICE_BONUS["child"][choices["child"]]
                    right = f"童年:{choices["child"]}\n{space_a}[{add}]"
                elif count == 4:
                    add = CHOICE_BONUS["dream"][choices["dream"]]
                    right = f"梦想:{choices["dream"]}\n{space_a}[{add}]"
                else:
                    right = "\n"
                # 拼接字符串
                line = " "*5 + left + right
                print(line)

                count += 1
            # 显示启动资金、商队配置、初始货物3个标题
            space = " "*((30-8)//2)  # 30-8的8是四字标题的长度，3个标题都是4个字所以通用
            left = f"{space}启动资金{space}"
            middle = f"{space}商队配置{space}"
            right = f"{space}初始货物"
            line = " "*5 + left + middle + right
            print(f"{Fore.YELLOW}{line}\n")
            # 显示具体的内容
            begin_money, team_config, carried_items = init_beginMoney_teamConfig_carriedItems(choices)
            # ==========左侧内容==========
            left_text = str(begin_money) + "第纳尔"
            left_space = " "*((30-str_length(left_text))//2)
            left = f"{left_space}{left_text}{left_space}"
            # ==========中间内容==========
            middle_text = "驮马*" + str(team_config["packhorse"]) + " 负重" + str(team_config["weight"]) + "kg"
            middle_space = " "*((30-str_length(middle_text))//2)
            middle = f"{middle_space}{middle_text}{middle_space}"
            # ==========右侧内容==========
            right_text = carried_items[0]["item"]["item_name"] + "*" + str(carried_items[0]["quantity"])
            right_space = " "*((30-str_length(right_text))//2)
            right = f"{right_space}{right_text}"
            # ==========拼接要打印的内容==========
            line = " "*5 + left + middle + right
            print(f"{Fore.CYAN}{line}")  # tip:打印内容行的时候把颜色改成蓝色
            change_color(Fore.GREEN)
            print_title("选项")
            print_center_text_default_color("1.开始游戏")
            print_center_text_default_color("2.重设经历")
            choice = input(center_space("选择:") + "选择:")
            if choice == "1":
                result, save_file_name = create_save_files(
                    player_name=choices["player_name"],
                    history_choices=choices,
                    begin_money=begin_money,
                    attributes=player_attributes,
                    team_config=team_config,
                    carried_items=carried_items
                )
                if result:  # 将游戏数据保存到存档中
                    return [True, save_file_name]
                else:  # 创建存档失败
                    clear_screen()
                    print_title(GAME_NAME)
                    print("\n\n\n")
                    print_center_text_default_color("创建存档出现问题，很抱歉给您带来的不便，请重试、反馈或重启游戏")
                    print("\n\n\n")
                    print_title(GAME_NAME)
                    input("按任意键继续...")
                    break
            elif choice == "2":
                break  # 结束信息展示页，回到外层循环，重新开始让玩家选择经历
    return None

# 点击加载存档后的再次确认界面
def confirm_load_save(save_file_dir: str):
    """
    确认加载存档界面
    :param save_file_dir: 存档名(目录)
    :return: True或False
    """
    while True:
        clear_screen()
        print_title(GAME_NAME)
        change_color(Fore.YELLOW)
        print("\n\n\n")
        print_center_text_default_color("确认")
        print()
        print_center_text_default_color(save_file_dir.replace("save\\", ""))
        print("\n\n\n")
        change_color(Fore.GREEN)
        print_title("选项")
        print_center_text_default_color("1. 确认    2. 返回")
        choice = input(center_space("选择:") + "选择:")
        if choice == "1":
            return True
        elif choice == "2":
            return False

# 开始游戏前的准备：初始化玩家、状态和地图对象，播放加载动画，然后进入游戏内主界面
def start_game(save_data: dict):
    """
    开始游戏的函数
    :return:
    """
    # 获取玩家对象并加载数据
    getPlayer().init_from_save_data(save_data)
    # 获取状态对象并加载数据
    getState().init_from_save_data(save_data)
    # 获取地图对象，然后显示玩家所在城市的那个区块
    getMap().init_player_location(getState().stay_city)
    # 播放加载动画
    for i in range(10):
        clear_screen()
        print_title(GAME_NAME)
        print("\n\n\n")
        change_color(Fore.YELLOW)
        print_center_text_default_color("正在进入中")
        print("\n\n\n")
        print(" "*5 + "-"*(9*(i+1)))
        change_color(Fore.GREEN)
        print_title(GAME_NAME)
        time.sleep(0.2)
    # 进入游戏内主界面
    gamePage_main()

# 进入游戏内主界面前的提示信息页面
def gamePage_tips():
    """
    首次游玩新存档显示的提示界面
    :return: 无
    """
    clear_screen()
    print_title(GAME_NAME)
    show_ui("media\\ui\\operation_tips_page.txt", Fore.YELLOW)
    print_title(GAME_NAME)
    input(center_space("关闭提示界面") + "关闭提示界面")

# 游戏内主界面
def gamePage_main():
    """
    游戏内主界面
    顶部是菜单栏，中间是地图，底部是另一个菜单栏
    :return: 无
    """
    # 玩家对象
    PLAYER = getPlayer()
    # 状态对象
    STATE = getState()
    # 地图对象
    MAP = getMap()
    # ====================提示界面====================
    if PLAYER.is_show_tips:
        # 修改is_show_tips为False，此后该存档不再显示提示界面
        PLAYER.tips_shown()
        # 提示界面
        gamePage_tips()
    # ====================游戏主界面====================
    def print_display():
        """
        游戏内主界面函数的子函数，主要负责更新并打印界面内容
        :return:
        """
        # ====================顶部边框====================
        print_top_title(GAME_NAME)
        # ====================顶部菜单(黄色)====================
        def top_menu():
            change_color(Fore.YELLOW)  # 改为黄色
            print("——" * 25)
            left = f'[地图:{MAP.now_block_code}]'
            season = ""
            if 1 <= STATE.date["month"] <= 3: season = "春"
            elif 4 <= STATE.date["month"] <= 6: season = "夏"
            elif 7 <= STATE.date["month"] <= 9: season = "秋"
            elif 10 <= STATE.date["month"] <= 12: season = "冬"
            day = ""
            if STATE.date["day"] == 1: day = "上旬"
            elif STATE.date["day"] == 2: day = "中旬"
            elif STATE.date["day"] == 3: day = "下旬"
            middle = f'[{season} {STATE.date["year"]}年-{STATE.date["month"]}月-{day}]'
            right = f'[{STATE.stay_city}]'
            # 先计算出来middle左右两边的space，再在左右两边的space中删除指定数量的空格然后拼接left和right
            left_space = (100 - str_length(middle)) // 2
            right_space = left_space
            left_space  = " " * (left_space  - str_length(left))
            right_space = " " * (right_space - str_length(right))
            print(left + left_space + middle + right_space + right)
            print("——" * 25)
        top_menu()
        # ====================中间地图(青色)====================
        def middle_map():
            change_color(Fore.CYAN)  # 改为青色
            for i in range(len(MAP.display)):
                print(FIVE_SPACE + MAP.display[i])
        middle_map()
        # ====================底部菜单(黄色)====================
        def bottom_menu():
            change_color(Fore.YELLOW)  # 改为黄色
            print("——" * 25)
            left = f'[人物|仓库|任务]'
            right = f'[${PLAYER.money}|{PLAYER.pack_weight}/{PLAYER.team_config["weight"]}kg|行动{STATE.action_point}/5]'
            space = " " * (100 - str_length(left) - str_length(right))
            print(left + space + right)
            print("——" * 25)
        bottom_menu()
        # ====================底部边框====================
        change_color(Fore.GREEN)
        print_bottom_title(GAME_NAME)
        # ====================游戏选项====================
        def options_menu():
            line1 = "1.人物 2.仓库 3.任务" + " "*(100-str_length("1.人物 2.仓库 3.任务地图 W.上S.下A.左D.右")) + "地图 W.上S.下A.左D.右"
            line2 = "4.资金 5.负重 6.行动" + " "*(100-str_length("4.资金 5.负重 6.行动7.回城 Q.退出 城市:id")) + "7.回城 Q.退出 城市:id"
            print(line1)
            print(line2)
        options_menu()
    options = ["1", "2", "3", "4", "5", "6", "7", "W", "A", "S", "D", "w", "a", "s", "d", "Q", "q"]
    while True:
        # 清屏
        clear_screen()
        # 显示界面
        print_display()
        # 输入选项
        choice = input(center_space("选择:") + "选择:")
        if choice in options:  # 判断是否是选项
            # 移动地图
            if choice in ["W", "w", "S", "s", "A", "a", "D", "d"]:
                MAP.move(choice)
            # 打开退出页
            elif choice == "Q" or choice == "q":
                choice = gamePage_quit()
                if choice == "quit":
                    # 保存游戏存档，并结束循环退回到主菜单
                    PLAYER.save_to_save_file()
                    STATE.save_to_save_file()
                    break
            # 回城选项(将地图回到玩家所在城市的地图)
            elif choice == "7":
                MAP.init_player_location(STATE.stay_city)
            # 人物页
            elif choice == "1":
                pass
            # 仓库页
            elif choice == "2":
                pass
            # 任务页
            elif choice == "3":
                pass
            # 资金页
            elif choice == "4":
                pass
            # 负重页
            elif choice == "5":
                pass
            # 行动页
            elif choice == "6":
                pass
        elif choice in MAP.now_towns.keys():  # 判断是否是城市编号
            print("选择了" + MAP.get_city_name_from_id(choice))
            time.sleep(2)
            pass
