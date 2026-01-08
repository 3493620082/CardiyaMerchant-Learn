# --coding=utf-8

from pygame import mixer
from src.funcs import *
from src.game import *

class Game:
    def __init__(self):
        # 读取配置
        self.CONFIG = read_config()
        # 初始化音乐
        self.init_music_and_sound()
        # 游戏启动界面
        self.start_game()
        # 游戏主菜单界面
        self.main_game_menu()

    def init_music_and_sound(self):
        mixer.init()
        mixer.music.load("media\\music\\background.ogg")
        mixer.music.set_volume(self.CONFIG["music_volume"] / 10)
        sound_list = []  # 音效列表，目前为空

    def start_game(self):
        clear_screen()
        show_ui("media\\ui\\start_page.txt")
        time.sleep(self.CONFIG["start_page_dealy_sec"])
        clear_screen()
        show_ui("media\\ui\\start_page_warning.txt")
        input(center_space("按下任意键开始") + "按下任意键开始")

    def main_game_menu(self):
        # 开始播放音乐
        mixer.music.play(-1)
        # 首页的几个选项
        options = ["1", "2", "3", "4", "5"]
        while True:
            clear_screen()
            print_title("卡迪亚行商")
            show_ui("media\\ui\\main_menu.txt", Fore.YELLOW)
            print_title("卡迪亚行商")
            choice = input(center_space("选择选项:") + "选择选项:")
            if choice in options:
                if choice == options[0]:
                    # 进入创建新游戏界面
                    self.new_game_page()
                elif choice == options[1]:
                    clear_screen()
                    # 进入读取存档界面
                    self.saves_page()
                elif choice == options[2]:
                    # 进入游戏设置界面
                    self.setting_page()
                elif choice == options[3]:
                    # 进入游戏成就界面
                    self.honor_page()
                elif choice == options[4]:
                    # 退出循环，结束游戏
                    break

    def new_game_page(self):
        """
        玩新游戏界面
        :return: 无
        """
        # 加载界面
        def aaa():
            clear_screen()
            for i in range(3):
                clear_screen()
                print_title("卡迪亚行商")
                print_center_text("加载中" + "."*(i+1))
                print_title("卡迪亚行商")
                time.sleep(0.5)
        aaa()
        # 背景故事
        def story():
            clear_screen()
            print_title(self.CONFIG["game_name"])
            for i in range(3): print()
            print_center_text("是否阅读背景故事(1是/0否)", Fore.YELLOW)
            for i in range(3): print()
            print_title(self.CONFIG["game_name"])
            choice = input(center_space("选择: ") + "选择: ")
            if choice != "0":  # 不等于0直接播放
                show_background_story()
        story()
        # 选择人物经历，初始化人物属性等，最后创建存档完成后返回True并开始游戏
        result, save_file_dir = gamePage_new_game()
        if result:
            # 读取存档数据并开始游戏
            save_data = load_save_data(save_file_dir)
            start_game(save_data)
        else:
            clear_screen()
            print_title("错误")
            print("\n\n\n")
            print_center_text("创建游戏失败，请反馈开发者", Fore.YELLOW)
            print("\n\n\n")
            print_title("错误")
            input()

        # 游戏结束后返回主界面
        return None

    def saves_page(self):
        """
        存档界面
        :return: 无
        """
        while True:
            clear_screen()
            print_title("存档列表")
            show_save_files()
            print_title("选项")
            print_center_text("返回主界面: -1")
            print_center_text("根据编号选择存档")
            # 获取存档列表
            save_list = load_save_files()
            try:
                choice = int(input(center_space("请选择:") + "请选择:"))
                if choice == -1:
                    return None  # 直接结束函数
                elif save_list[choice - 1] in save_list:  # 如果所选存档存在
                    # 显示确认界面，确认加载存档
                    result = confirm_load_save(save_list[choice - 1])
                    if result:
                        break
                else:  # 所选存档不存在
                    print("选择的存档不存在!")
                    time.sleep(2)
            except Exception:
                print("输入有误!")
                time.sleep(2)

        # 读取存档数据并开始游戏
        save_data = load_save_data(save_list[choice - 1])
        start_game(save_data)
        # 游戏结束后返回主界面
        return None

    def setting_page(self):
        """
        游戏设置界面
        :return: 无
        """
        while True:
            clear_screen()
            print_title("游戏设置")
            print(Fore.YELLOW, end="")
            print(" "*5 + "-  调整字体大小: Ctrl+鼠标滚轮")
            print(" "*5 + "-  设置字体: 右键窗口->属性->字体")
            print()
            print(" "*5 + "1. 音乐音量[0-10]: " + str(self.CONFIG["music_volume"]))
            print(" "*5 + "2. 音效音量[0-10]: " + str(self.CONFIG["sound_volume"]))
            print(Fore.GREEN, end="")
            print_title("选项")
            print_center_text("返回主界面: -1")
            print_center_text("根据编号选择选项")
            try:
                choice = int(input("选项选项: "))
                if choice == -1:  # 返回主界面
                    break
                elif choice == 1:  # 修改音乐音量
                    vol = int(input("输入数值: "))
                    if vol < 0: vol = 0
                    elif vol > 10: vol = 10
                    self.CONFIG["music_volume"] = vol
                    mixer.music.set_volume(vol / 10)
                    write_config(self.CONFIG)
                elif choice == 2:  # 修改音效音量
                    vol = int(input("输入数值: "))
                    if vol < 0: vol = 0
                    elif vol > 10: vol = 10
                    self.CONFIG["sound_volume"] = vol
                    # TODO: 等这里有音效了，遍历音效列表中的所有音效，为每个音效设置音量
                    write_config(self.CONFIG)
            except Exception:
                print("输入有误!")
                time.sleep(2)

    def honor_page(self):
        clear_screen()
        print_title("成就界面")
        show_honor()
        print_title("成就界面")
        input("按下任意键返回")

if __name__ == '__main__':
    Game()
