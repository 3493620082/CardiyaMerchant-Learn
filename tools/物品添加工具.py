import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

# 定义大写常量列表，存放物品类型选项（方便后续更新）
ITEM_TYPES = [
    "食物",
    "衣物",
    "纺织品",
    "矿物",
    "材料",
    "魔法道具",
    "奢侈品",
    "工具",
    "武器",
    "其它"
]

def load_items():
    """加载items.json中的数据"""
    json_path = os.path.join("..", "src", "data", "items.json")
    if not os.path.exists(json_path):
        # 若文件不存在，初始化空结构
        return {"items": []}
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_items(data):
    """保存数据到items.json"""
    json_path = os.path.join("..", "src", "data", "items.json")
    # 确保目录存在
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def generate_item_id(items):
    """生成不重复的item_id"""
    if not items:
        return 1
    # 先获取当前最大id+1
    current_ids = [item["item_id"] for item in items]
    new_id = max(current_ids) + 1
    # 检查是否重复（防止手动修改导致的id混乱）
    while new_id in current_ids:
        new_id += 1
    return new_id

def add_item():
    """添加物品的核心函数"""
    # 获取输入值
    item_name = entry_name.get().strip()
    item_desc = entry_desc.get().strip() or "该物品暂时没有描述"
    price_input = entry_price.get().strip()
    weight_input = entry_weight.get().strip()
    item_type = combo_type.get()  # 从下拉框获取选中的类型

    # 验证1：物品名不能为空
    if not item_name:
        messagebox.showerror("错误", "物品名不能为空！")
        return

    # 验证2：价格（非空、非负）
    try:
        price = float(price_input)
        if price < 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("错误", "价格必须是不小于0的数字！")
        return

    # 验证3：重量（非空、大于0）
    try:
        weight = float(weight_input)
        if weight <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("错误", "重量必须是大于0的数字！")
        return

    # 验证4：类型必须选择
    if not item_type:
        messagebox.showerror("错误", "请选择物品类型！")
        return

    # 加载现有数据
    data = load_items()
    items = data["items"]

    # 生成item_id
    new_id = generate_item_id(items)

    # 构造新物品
    new_item = {
        "item_id": new_id,
        "item_name": item_name,
        "desc": item_desc,
        "price": price,
        "weight": weight,
        "type": item_type
    }

    # 添加并保存
    items.append(new_item)
    save_items(data)
    messagebox.showinfo("成功", f"物品“{item_name}”添加完成！ID：{new_id}")
    clear_input()

def clear_input():
    """清空输入框"""
    entry_name.delete(0, tk.END)
    entry_desc.delete(0, tk.END)
    entry_price.delete(0, tk.END)
    entry_weight.delete(0, tk.END)
    combo_type.set("")  # 清空下拉框

# 主界面
root = tk.Tk()
root.title("物品添加工具")
root.geometry("400x300")

# 控件布局
tk.Label(root, text="物品名：").grid(row=0, column=0, padx=10, pady=10, sticky="w")
entry_name = tk.Entry(root, width=30)
entry_name.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="物品描述：").grid(row=1, column=0, padx=10, pady=5, sticky="w")
entry_desc = tk.Entry(root, width=30)
entry_desc.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="价格：").grid(row=2, column=0, padx=10, pady=5, sticky="w")
entry_price = tk.Entry(root, width=30)
entry_price.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="重量：").grid(row=3, column=0, padx=10, pady=5, sticky="w")
entry_weight = tk.Entry(root, width=30)
entry_weight.grid(row=3, column=1, padx=10, pady=5)

# 类型下拉框（使用大写常量列表）
tk.Label(root, text="类型：").grid(row=4, column=0, padx=10, pady=5, sticky="w")
combo_type = ttk.Combobox(root, values=ITEM_TYPES, width=28, state="readonly")
combo_type.grid(row=4, column=1, padx=10, pady=5)

# 按钮
btn_add = tk.Button(root, text="添加", width=10, command=add_item)
btn_add.grid(row=5, column=0, padx=10, pady=20)

btn_clear = tk.Button(root, text="清空", width=10, command=clear_input)
btn_clear.grid(row=5, column=1, padx=10, pady=20)

root.mainloop()
