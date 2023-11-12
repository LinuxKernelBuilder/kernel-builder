#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import re
import time
import os
import tkinter as tk
from tkinter import Menu, messagebox
import subprocess

def get_latest_kernel():
    global latest_kernel_label
    global current_kernel_label
    latest_kernel = None
    try:
        response = requests.get("https://www.kernel.org/")
        latest_kernel = re.search(r"\d+\.\d+\.\d+", response.text).group()
        latest_kernel_label.config(text=f"Latest mainline-Linux kernel version: {latest_kernel}")
    except requests.exceptions.RequestException as e:
        latest_kernel_label.config(text=f"Failed to fetch kernel info: {e}")
    except AttributeError as e:
        latest_kernel_label.config(text=f"Failed to match kernel version: {e}")

    try:
        with open("get_latest_kernel.txt", "w") as f:
            f.write(str(latest_kernel))
            print(f"Latest mainline-Linux kernel version exported to get_latest_kernel.txt")
    except IOError as e:
        latest_kernel_label.config(text=f"Failed to write to file: {e}")

    current_kernel = None
    try:
        current_kernel = re.search(r"\d+\.\d+\.\d+", os.popen("uname -r").read()).group()
        current_kernel_label.config(text=f"Current mainline-Linux kernel version: {current_kernel}")
    except OSError as e:
        current_kernel_label.config(text=f"Failed to get kernel version: {e}")
    except AttributeError as e:
        current_kernel_label.config(text=f"Failed to match kernel version: {e}")

    if latest_kernel and current_kernel:
        if latest_kernel > current_kernel:
            latest_kernel_label.config(text=f"New kernel version available: **{latest_kernel}**", fg="red")
        elif latest_kernel <= current_kernel:
            latest_kernel_label.config(text="Current kernel version is up to date", fg="green")

def execute_script():
    try:
        os.system("chmod +x script.sh")
        os.system("./script.sh")
        print("script.sh executed successfully")
    except Exception as e:
        print(f"Failed to execute script.sh: {e}")

def execute_time_script():
    try:
        subprocess.run(["python3", "time.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Script execution failed: {e}")
        latest_kernel_label.config(text=f"Script execution failed: {e}")

def about():
    tk.messagebox.showinfo("About", "This program was created by Kernel-Builder SIG.\nKernel versions are sourced from https://www.kernel.org/.")

window = tk.Tk()
window.title("Get Latest Linux Kernel Version")
window.geometry("600x400")

button1 = tk.Button(window, text="Get Latest Kernel Version", command=get_latest_kernel)
button1.pack(pady=10)

button2 = tk.Button(window, text="Execute script.sh", command=execute_script)
button2.pack(pady=10)

execute_button = tk.Button(window, text="Execute time.py script", command=execute_time_script)
execute_button.pack(pady=10)

latest_kernel_label = tk.Label(window, text="Latest mainline-Linux kernel version: ")
latest_kernel_label.pack(pady=5)

current_kernel_label = tk.Label(window, text="Current mainline-Linux kernel version: ")
current_kernel_label.pack(pady=5)

author_label = tk.Label(window, text="Author: Kernel-Builder SIG")
author_label.pack(side=tk.LEFT, padx=10)

source_label = tk.Label(window, text="Kernel version source: https://www.kernel.org/")
source_label.pack(side=tk.RIGHT, padx=10)

# Menu Bar
menu_bar = Menu(window)
window.config(menu=menu_bar)

# About Menu
about_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="About", menu=about_menu)
about_menu.add_command(label="Info", command=about)

window.mainloop()
