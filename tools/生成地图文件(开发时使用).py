import json
import random

"""
该Python文件只允许在开发时使用，游戏制作完成后禁止再次调用，可能会破坏原有逻辑
"""

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

# 定义25个区块的完整数据（和之前分配的一致）
map_blocks = {
    "1-1": {
        "block_code": "1-1",
        "grid_position": {"row": 1, "col": 1},
        "towns": ["珀特洛斯堡", "弗兰迪亚斯", "香料镇"],
        "town_count": 3
    },
    "1-2": {
        "block_code": "1-2",
        "grid_position": {"row": 1, "col": 2},
        "towns": ["加伦港", "阿加莎隆", "丝绸镇"],
        "town_count": 3
    },
    "1-3": {
        "block_code": "1-3",
        "grid_position": {"row": 1, "col": 3},
        "towns": ["果酿镇", "暖阳镇", "椰枣村"],
        "town_count": 3
    },
    "1-4": {
        "block_code": "1-4",
        "grid_position": {"row": 1, "col": 4},
        "towns": ["帆影镇", "麦仓镇", "棉麻村"],
        "town_count": 3
    },
    "1-5": {
        "block_code": "1-5",
        "grid_position": {"row": 1, "col": 5},
        "towns": ["瓷瓦镇", "橘园村", "渔获村"],
        "town_count": 3
    },
    "2-1": {
        "block_code": "2-1",
        "grid_position": {"row": 2, "col": 1},
        "towns": ["蔗田村", "陶土村", "香草村"],
        "town_count": 3
    },
    "2-2": {
        "block_code": "2-2",
        "grid_position": {"row": 2, "col": 2},
        "towns": ["稻花村", "木舟村", "盐场村"],
        "town_count": 3
    },
    "2-3": {
        "block_code": "2-3",
        "grid_position": {"row": 2, "col": 3},
        "towns": ["高尔多瓦", "黑铁城", "羊毛村"],
        "town_count": 3
    },
    "2-4": {
        "block_code": "2-4",
        "grid_position": {"row": 2, "col": 4},
        "towns": ["巴德林", "雪矛镇", "冻土村"],
        "town_count": 3
    },
    "2-5": {
        "block_code": "2-5",
        "grid_position": {"row": 2, "col": 5},
        "towns": ["加德蒙", "寒毡镇", "雪粮村"],
        "town_count": 3
    },
    "3-1": {
        "block_code": "3-1",
        "grid_position": {"row": 3, "col": 1},
        "towns": ["洛萨维", "凛风镇", "护墙村"],
        "town_count": 3
    },
    "3-2": {
        "block_code": "3-2",
        "grid_position": {"row": 3, "col": 2},
        "towns": ["铁砧镇", "熔铁村", "暖炉村"],
        "town_count": 3
    },
    "3-3": {
        "block_code": "3-3",
        "grid_position": {"row": 3, "col": 3},
        "towns": ["驯鹿村", "冰溪村", "奥斯峡"],
        "town_count": 3
    },
    "3-4": {
        "block_code": "3-4",
        "grid_position": {"row": 3, "col": 4},
        "towns": ["卑尔索", "迷雾镇", "蕨草村"],
        "town_count": 3
    },
    "3-5": {
        "block_code": "3-5",
        "grid_position": {"row": 3, "col": 5},
        "towns": ["特隆海姆", "药草镇", "菌菇村"],
        "town_count": 3
    },
    "4-1": {
        "block_code": "4-1",
        "grid_position": {"row": 4, "col": 1},
        "towns": ["罗瓦峡湾", "卷轴镇", "松脂村"],
        "town_count": 3
    },
    "4-2": {
        "block_code": "4-2",
        "grid_position": {"row": 4, "col": 2},
        "towns": ["橡木镇", "炼金镇", "晶矿村"],
        "town_count": 3
    },
    "4-3": {
        "block_code": "4-3",
        "grid_position": {"row": 4, "col": 3},
        "towns": ["星木镇", "藤蔓村", "萤火村"],
        "town_count": 3
    },
    "4-4": {
        "block_code": "4-4",
        "grid_position": {"row": 4, "col": 4},
        "towns": ["石磨村", "蜂蜡村", "枯木村"],
        "town_count": 3
    },
    "4-5": {
        "block_code": "4-5",
        "grid_position": {"row": 4, "col": 5},
        "towns": ["苏哈尔港", "戈壁镇", "胡杨村"],
        "town_count": 3
    },
    "5-1": {
        "block_code": "5-1",
        "grid_position": {"row": 5, "col": 1},
        "towns": ["卡布斯堡", "商驿镇", "沙枣村"],
        "town_count": 3
    },
    "5-2": {
        "block_code": "5-2",
        "grid_position": {"row": 5, "col": 2},
        "towns": ["萨哈尔麦纳", "瓷茶镇", "清泉村"],
        "town_count": 3
    },
    "5-3": {
        "block_code": "5-3",
        "grid_position": {"row": 5, "col": 3},
        "towns": ["法赫尔丁", "沙棘镇", "棉花村"],
        "town_count": 3
    },
    "5-4": {
        "block_code": "5-4",
        "grid_position": {"row": 5, "col": 4},
        "towns": ["驼铃镇", "硝石镇", "铜砂村"],
        "town_count": 3
    },
    "5-5": {
        "block_code": "5-5",
        "grid_position": {"row": 5, "col": 5},
        "towns": ["绿洲镇", "风旗镇", "帐篷村", "驿站村"],
        "town_count": 4
    }
}

# 遍历所有区块，创建并写入JSON文件
for block_name, block_data in map_blocks.items():
    # 文件名：区块编号.json（如1-1.json）
    file_name = f"..\\media\\block\\{block_name}.json"
    # display键
    lines = []
    town_to_lines = random.sample(range(15), len(block_data["towns"]))
    lines = [""] * 15
    for i in range(len(town_to_lines)):
        l_index = town_to_lines[i]  # 行数的索引
        town = block_data["towns"][i]  # 城镇
        random_space = " " * random.randint(0, 90-(str_length(town)))
        lines[l_index] = random_space + block_data["towns"][i]
    block_data["display"] = lines
    # 写入文件，ensure_ascii=False保证中文正常显示，indent=2让格式更美观
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(block_data, f, ensure_ascii=False, indent=4)
    print(f"成功创建文件：{file_name}")

print("\n所有25个地图区块JSON文件已创建完成！")
