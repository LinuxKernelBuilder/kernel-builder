#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 获取最新的Linux内核版本
import requests
import re
import time
import os
import tkinter as tk
import subprocess

# 定义一个函数，用于获取最新的内核版本，并且和当前的内核版本进行比较
def get_latest_kernel():
    global latest_kernel_label # 使用全局变量
    global current_kernel_label
    latest_kernel = None # 给 latest_kernel 赋一个初始值
    try:
        response = requests.get("https://www.kernel.org/")
        # 修改正则表达式，匹配以数字开头并且包含小数点的字符串
        latest_kernel = re.search(r"\d+\.\d+\.\d+", response.text).group()
        print(f"最新的mainlineLinux-内核版本是{latest_kernel}")
        latest_kernel_label.config(text=f"最新的mainline-Linux内核版本是：{latest_kernel}") # 更新标签上的文本
    except requests.exceptions.RequestException as e:
        print(f"请求内核官网失败：{e}")
        latest_kernel_label.config(text=f"请求内核官网失败：{e}") # 更新标签上的文本
    except AttributeError as e:
        print(f"匹配内核版本失败：{e}")
        latest_kernel_label.config(text=f"匹配内核版本失败：{e}") # 更新标签上的文本
    # 将最新的内核版本写入到文件中
    try:
        with open("get_latest_kernel.txt", "w") as f: # 以写入模式打开文件
            f.write(str(latest_kernel)) # 写入最新的内核版本，转换为字符串类型
            print(f"已将最新的mainline-Linux内核版本导出到 get_latest_kernel.txt 文件中")
    except IOError as e:
        print(f"写入文件失败：{e}")
        latest_kernel_label.config(text=f"写入文件失败：{e}") # 更新标签上的文本
    # 获取当前的Linux内核版本
    current_kernel = None # 给 current_kernel 赋一个初始值
    try:
        # 修改正则表达式，匹配以数字开头并且包含小数点的字符串
        current_kernel = re.search(r"\d+\.\d+\.\d+", os.popen("uname -r").read()).group()
        print(f"当前的mainline-Linux内核版本是：{current_kernel}")
        current_kernel_label.config(text=f"当前的mainline-Linux内核版本是：{current_kernel}") # 更新标签上的文本
    except OSError as e:
        print(f"获取内核版本失败：{e}")
        current_kernel_label.config(text=f"获取内核版本失败：{e}") # 更新标签上的文本
    except AttributeError as e:
        print(f"匹配内核版本失败：{e}")
        current_kernel_label.config(text=f"匹配内核版本失败：{e}") # 更新标签上的文本

    # 比较最新的内核版本和当前的内核版本，如果有更新，提示用户
    if latest_kernel and current_kernel: # 如果两个变量都不为空
        if latest_kernel > current_kernel: # 如果最新的内核版本大于当前的内核版本
            latest_kernel_label.config(text=f"有新的内核版本可用：**{latest_kernel}**", fg="red") # 更新标签上的文本，并显示最新的内核版本，用红色字体
        elif latest_kernel <= current_kernel: # 如果最新的内核版本等于或小于当前的内核版本
            latest_kernel_label.config(text=f"当前的内核版本已经是最新的", fg="green") # 更新标签上的文本，用绿色字体

def execute_script():
    try:
        os.system("chmod +x script.sh")  # 添加执行权限
        os.system("./script.sh")  # Execute the script.sh file
        print("script.sh 执行成功")
    except Exception as e:
        print(f"执行 script.sh 失败：{e}")

# 定义一个函数，用于执行time.py脚本
def execute_time_script():
    try:
        subprocess.run(["python3", "time.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"执行脚本失败：{e}")
        latest_kernel_label.config(text=f"执行脚本失败：{e}") # 更新标签上的文本


# 创建一个窗口
window = tk.Tk()
window.title("获取最新的Linux内核版本") # 设置窗口标题
window.geometry("600x350") # 设置窗口大小

# 创建一个按钮，点击时调用get_latest_kernel函数
button1 = tk.Button(window, text="获取最新的内核版本", command=get_latest_kernel)
button1.pack() # 将按钮添加到窗口中

# 创建一个按钮，点击时执行 script.sh 脚本
button2 = tk.Button(window, text="执行 script.sh", command=execute_script)
button2.pack() # 将按钮添加到窗口中

# 创建一个按钮，用于执行time.py脚本
execute_button = tk.Button(window, text="执行time.py脚本", command=execute_time_script)
execute_button.pack() # 将按钮添加到窗口中

# 创建两个标签，用于显示最新的内核版本和当前的内核版本
latest_kernel_label = tk.Label(window, text="最新的mainline-Linux内核版本是：")
latest_kernel_label.pack() # 将标签添加到窗口中
current_kernel_label = tk.Label(window, text="当前的Linux内核版本是：")
current_kernel_label.pack() # 将标签添加到窗口中

# 创建两个标签，用于显示作者信息和内核版本来源
author_label = tk.Label(window, text="作者:Kernel-Builder SIG")
author_label.pack(side=tk.LEFT) # 将标签添加到窗口中，并放在左边
source_label = tk.Label(window, text="内核版本来源：https://www.kernel.org/")
source_label.pack(side=tk.RIGHT) # 将标签添加到窗口中，并放在右边

# 进入主循环，等待用户操作
window.mainloop()