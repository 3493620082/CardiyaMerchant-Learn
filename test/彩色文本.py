from colorama import init, Fore, Back, Style
# 初始化colorama（自动启用CMD的ANSI支持）
init(autoreset=True)  # autoreset=True自动重置样式，不用手动加RESET

# 直接用语义化的常量输出
print(Fore.RED + "红色文字")
print(Style.BRIGHT + Fore.RED + "加粗红色文字")
print(Back.GREEN + "绿色背景的默认文字")
print(Fore.YELLOW + "黄色文字 + " + Fore.MAGENTA + "紫色文字（混合使用）")