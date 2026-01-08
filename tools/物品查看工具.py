import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import subprocess
import sys

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

# -------------------------- 核心数据处理函数 --------------------------
def load_items():
    """加载items.json中的物品数据"""
    json_path = os.path.join("..", "src", "data", "items.json")
    if not os.path.exists(json_path):
        return {"items": []}
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        messagebox.showerror("错误", "items.json文件格式错误！")
        return {"items": []}


def save_items(data):
    """保存修改后的数据到items.json"""
    json_path = os.path.join("..", "src", "data", "items.json")
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def refresh_treeview(tree):
    """刷新TreeView列表"""
    # 清空现有数据
    for item in tree.get_children():
        tree.delete(item)
    # 加载最新数据并插入
    data = load_items()
    for item in data["items"]:
        tree.insert("", tk.END, values=(
            item["item_id"],
            item["item_name"],
            item["desc"],
            item["price"],
            item["weight"],
            item["type"]
        ), tags=(item["item_id"],))


# -------------------------- 事件处理函数 --------------------------
def on_tree_select(event, tree, entry_name, entry_desc, entry_price, entry_weight, combobox_type):
    """点击TreeView行时填充输入框"""
    selected = tree.selection()
    if not selected:
        return
    # 获取选中行的数据
    item_data = tree.item(selected[0])["values"]
    # 填充到输入框
    entry_name.delete(0, tk.END)
    entry_name.insert(0, item_data[1])

    entry_desc.delete(0, tk.END)
    entry_desc.insert(0, item_data[2])

    entry_price.delete(0, tk.END)
    entry_price.insert(0, item_data[3])

    entry_weight.delete(0, tk.END)
    entry_weight.insert(0, item_data[4])

    # 填充分类下拉框
    combobox_type.set(item_data[5])


def modify_item(tree, entry_name, entry_desc, entry_price, entry_weight, combobox_type):
    """修改选中物品"""
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("提示", "请先选中要修改的物品！")
        return

    # 获取选中物品的ID和输入框数据
    item_data = tree.item(selected[0])["values"]
    item_id = int(item_data[0])
    new_name = entry_name.get().strip()
    new_desc = entry_desc.get().strip() or "该物品暂时没有描述"
    new_price = entry_price.get().strip()
    new_weight = entry_weight.get().strip()
    # 从下拉框获取分类（支持手动输入）
    new_type = combobox_type.get().strip() or "其它"

    # 验证输入合法性
    if not new_name:
        messagebox.showerror("错误", "物品名不能为空！")
        return

    try:
        new_price = float(new_price)
        if new_price < 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("错误", "价格必须是不小于0的数字！")
        return

    try:
        new_weight = float(new_weight)
        if new_weight <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("错误", "重量必须是大于0的数字！")
        return

    # 确认修改
    if not messagebox.askyesno("确认", "确定要修改该物品信息吗？"):
        return

    # 加载数据并修改
    data = load_items()
    for idx, item in enumerate(data["items"]):
        if item["item_id"] == item_id:
            data["items"][idx] = {
                "item_id": item_id,
                "item_name": new_name,
                "desc": new_desc,
                "price": new_price,
                "weight": new_weight,
                "type": new_type
            }
            break

    # 保存并刷新
    save_items(data)
    refresh_treeview(tree)
    messagebox.showinfo("成功", "物品信息修改完成！")


def delete_item(tree):
    """删除选中物品"""
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("提示", "请先选中要删除的物品！")
        return

    # 获取选中物品ID和名称
    item_data = tree.item(selected[0])["values"]
    item_id = int(item_data[0])
    item_name = item_data[1]

    # 确认删除
    if not messagebox.askyesno("确认", f"确定要删除物品【{item_name}】吗？"):
        return

    # 加载数据并删除
    data = load_items()
    data["items"] = [item for item in data["items"] if item["item_id"] != item_id]

    # 保存并刷新
    save_items(data)
    refresh_treeview(tree)
    messagebox.showinfo("成功", f"物品【{item_name}】已删除！")


def open_add_tool():
    """打开物品添加工具"""
    try:
        # 启动同一目录下的添加工具（假设添加工具文件名为item_add_tool.py）
        script_path = os.path.join(os.path.dirname(__file__), "物品添加工具.py")
        # 兼容不同Python环境
        subprocess.Popen([sys.executable, script_path])
    except FileNotFoundError:
        messagebox.showerror("错误", "未找到物品添加工具文件（item_add_tool.py）！")
    except Exception as e:
        messagebox.showerror("错误", f"启动添加工具失败：{str(e)}")


def refresh_items(tree):
    """刷新物品列表（重新读取文件并更新）"""
    try:
        refresh_treeview(tree)
        messagebox.showinfo("成功", "列表已刷新！")
    except Exception as e:
        messagebox.showerror("错误", f"刷新失败：{str(e)}")


# -------------------------- 界面构建 --------------------------
def main():
    root = tk.Tk()
    root.title("物品管理工具")

    # 1. 创建TreeView框架
    frame_tree = ttk.Frame(root)
    frame_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # 创建TreeView
    columns = ("id", "物品名", "描述", "价格", "重量", "分类")
    tree = ttk.Treeview(frame_tree, columns=columns, show="headings", height=20)

    # 设置列标题和宽度
    tree.heading("id", text="ID")
    tree.heading("物品名", text="物品名")
    tree.heading("描述", text="描述")
    tree.heading("价格", text="价格")
    tree.heading("重量", text="重量")
    tree.heading("分类", text="分类")

    tree.column("id", width=50, anchor="center")
    tree.column("物品名", width=150, anchor="w")
    tree.column("描述", width=300, anchor="w")
    tree.column("价格", width=80, anchor="center")
    tree.column("重量", width=80, anchor="center")
    tree.column("分类", width=80, anchor="center")

    # 滚动条
    scroll_y = ttk.Scrollbar(frame_tree, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scroll_y.set)

    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

    # 2. 创建输入框框架
    frame_input = ttk.Frame(root)
    frame_input.pack(fill=tk.X, padx=10, pady=5)

    # 输入框布局（一行一个，对齐排列）
    labels = ["物品名：", "物品描述：", "价格：", "重量：", "分类："]
    entries = []

    for idx, label_text in enumerate(labels):
        frame_row = ttk.Frame(frame_input)
        frame_row.pack(fill=tk.X, padx=20, pady=3)

        lbl = ttk.Label(frame_row, text=label_text, width=10, anchor="w")
        lbl.pack(side=tk.LEFT)

        # 分类项使用Combobox（下拉选择框）
        if idx == 4:
            entry = ttk.Combobox(frame_row, values=ITEM_TYPES, state="readonly")
            # 设置默认值
            entry.set("其它")
        else:
            entry = ttk.Entry(frame_row)

        entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        entries.append(entry)

    # 解包输入框/下拉框
    entry_name, entry_desc, entry_price, entry_weight, combobox_type = entries

    # 3. 创建按钮框架
    frame_btn = ttk.Frame(root)
    frame_btn.pack(fill=tk.X, padx=10, pady=10)

    # 左侧按钮区域
    frame_btn_left = ttk.Frame(frame_btn)
    frame_btn_left.pack(side=tk.LEFT)

    btn_modify = ttk.Button(frame_btn_left, text="修改", width=15,
                            command=lambda: modify_item(tree, entry_name, entry_desc, entry_price, entry_weight,
                                                        combobox_type))
    btn_delete = ttk.Button(frame_btn_left, text="删除", width=15, command=lambda: delete_item(tree))
    btn_add_tool = ttk.Button(frame_btn_left, text="物品添加工具", width=15, command=open_add_tool)

    btn_modify.pack(side=tk.LEFT, padx=20)
    btn_delete.pack(side=tk.LEFT, padx=20)
    btn_add_tool.pack(side=tk.LEFT, padx=20)

    # 右侧刷新按钮区域
    frame_btn_right = ttk.Frame(frame_btn)
    frame_btn_right.pack(side=tk.RIGHT)

    btn_refresh = ttk.Button(frame_btn_right, text="刷新列表", width=15,
                             command=lambda: refresh_items(tree))
    btn_refresh.pack(side=tk.RIGHT, padx=20)

    # 绑定TreeView选中事件（更新下拉框）
    tree.bind("<<TreeviewSelect>>",
              lambda e: on_tree_select(e, tree, entry_name, entry_desc, entry_price, entry_weight, combobox_type))

    # 初始化加载数据
    refresh_treeview(tree)

    root.mainloop()


if __name__ == "__main__":
    main()