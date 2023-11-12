import os
import tkinter as tk
from tkinter import Menu, messagebox

def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    window.geometry(f"{width}x{height}+{x}+{y}")

def get_latest_kernel(branch):
    global latest_kernel_label
    global current_kernel_label

    # Define the file path based on the specified branch
    file_path = f"txt/{branch}.txt"

    try:
        with open(file_path, "r") as f:
            latest_kernel = f.read().strip()
            latest_kernel_label.config(text=f"Latest {branch.capitalize()} kernel version: {latest_kernel}")
    except FileNotFoundError:
        latest_kernel_label.config(text=f"File not found: {file_path}")
    except Exception as e:
        latest_kernel_label.config(text=f"Error reading file: {e}")

    current_kernel = None
    try:
        current_kernel = os.popen("uname -r").read().strip()
        current_kernel_label.config(text=f"Current {branch.capitalize()} kernel version: {current_kernel}")
    except Exception as e:
        current_kernel_label.config(text=f"Failed to get kernel version: {e}")

    if latest_kernel and current_kernel:
        if latest_kernel > current_kernel:
            latest_kernel_label.config(text=f"New kernel version available: **{latest_kernel}**", fg="red")
        elif latest_kernel <= current_kernel:
            latest_kernel_label.config(text=f"Current kernel version is up to date", fg="green")

def execute_script():
    try:
        os.system("chmod +x script.sh")
        os.system("./script.sh")
        print("script.sh executed successfully")
    except Exception as e:
        print(f"Failed to execute script.sh: {e}")

def execute_time_script():
    try:
        os.system("python3 time.py")
    except Exception as e:
        print(f"Script execution failed: {e}")
        latest_kernel_label.config(text=f"Script execution failed: {e}")

def about():
    tk.messagebox.showinfo("About", "This program was created by Kernel-Builder SIG.\nKernel versions are sourced from txt files in the current directory.")

def update_window_size(event):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    window_size_label.config(text=f"Window Size: {width} x {height}")

window = tk.Tk()
window.title("Get Latest Linux Kernel Version")
window.geometry("1000x420")

# Center the window
center_window(window)

# Logo
logo_path = "image/LinuxKernelBuilder-logo.png"
if os.path.exists(logo_path):
    logo = tk.PhotoImage(file=logo_path)
    window.iconphoto(True, logo)

button_longterm = tk.Button(window, text="Get Latest Longterm Kernel Version", command=lambda: get_latest_kernel("longterm"))
button_longterm.pack(pady=10)

button_mainline = tk.Button(window, text="Get Latest Mainline Kernel Version", command=lambda: get_latest_kernel("mainline"))
button_mainline.pack(pady=10)

button_stable = tk.Button(window, text="Get Latest Stable Kernel Version", command=lambda: get_latest_kernel("stable"))
button_stable.pack(pady=10)

button2 = tk.Button(window, text="Execute script.sh", command=execute_script)
button2.pack(pady=10)

execute_button = tk.Button(window, text="Execute time.py script", command=execute_time_script)
execute_button.pack(pady=10)

latest_kernel_label = tk.Label(window, text="Latest kernel version: ")
latest_kernel_label.pack(pady=5)

current_kernel_label = tk.Label(window, text="Current kernel version: ")
current_kernel_label.pack(pady=5)

window_size_label = tk.Label(window, text="Window Size: 0 x 0")
window_size_label.pack(side=tk.BOTTOM, pady=5)

author_label = tk.Label(window, text="Author: Kernel-Builder SIG")
author_label.pack(side=tk.LEFT, padx=10)

source_label = tk.Label(window, text="Kernel version source: txt files in the current directory")
source_label.pack(side=tk.RIGHT, padx=10)

# Menu Bar
menu_bar = Menu(window)
window.config(menu=menu_bar)

# About Menu
about_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="About", menu=about_menu)
about_menu.add_command(label="Info", command=about)

# Bind window resize event
window.bind("<Configure>", update_window_size)

window.mainloop()
