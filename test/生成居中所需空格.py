while True:
    s = input("输入文本: ")
    length = 0
    for ch in s:
        if ord(ch) <= 127:
            length += 1
        else:
            length += 2
    print("}" + " "*((100 - length) // 2) + "{")