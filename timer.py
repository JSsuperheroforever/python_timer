import tkinter as tk
import time
import pytz
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageTk
import pystray
from pystray import MenuItem as item
import threading
from tkinter import messagebox
import sys
import pkg_resources
"""
桌面时钟 V0.0.1
"""

# 创建根窗口
root = tk.Tk()
root.title("北京时间")
root.geometry("400x200")

# 设置窗口透明，去除框架和按钮
root.attributes("-topmost", True)  # 窗口始终位于最前面
root.attributes("-transparentcolor", "white")  # 设置黑色为透明色
root.configure(bg='white')  # 设置背景为黑色

# 去除窗口的框架和按钮
root.overrideredirect(True)

# 获取屏幕的宽度和高度
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# 计算根窗口的位置，放置在右上角
window_width = 400
window_height = 200
x_position = screen_width - window_width  # 屏幕右边
y_position = 0  # 屏幕顶部
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# 创建Label用于显示时间
time_label = tk.Label(root, bg='white')
time_label.pack(expand=True)

# 设置字体和透明度
def create_transparent_text_image(time_text):
    # 创建一个透明背景的图像
    img = Image.new("RGBA", (400, 100), (0, 0, 0, 0))  # RGBA模式（包括透明度）
    draw = ImageDraw.Draw(img)

    # 使用Arial字体
    font = ImageFont.truetype("arial.ttf", 80)

    # 设置字体颜色
    draw.text((50, 25), time_text, font=font, fill=(255, 255, 0, 255))  # 黄色，100%透明度
    return img

# 获取北京时间并更新显示
def update_time():
    # 获取北京时间
    tz = pytz.timezone('Asia/Shanghai')
    current_time = datetime.now(tz).strftime('%H:%M:%S')

    # 创建半透明时钟图像
    img = create_transparent_text_image(current_time)

    # 将PIL图像转换为Tkinter可以显示的图像
    tk_img = ImageTk.PhotoImage(img)

    # 更新标签显示的图像
    time_label.config(image=tk_img)
    time_label.image = tk_img  # 保存引用，防止图片被垃圾回收

    # 每隔1000毫秒更新一次
    time_label.after(1000, update_time)

# 添加拖动窗口的功能
def on_press(event):
    global x_offset, y_offset
    x_offset = event.x
    y_offset = event.y

def on_drag(event):
    _x = event.x - x_offset
    _y = event.y - y_offset
    new_x = root.winfo_x() + _x
    new_y = root.winfo_y() + _y
    root.geometry(f"+{new_x}+{new_y}")

# 记录鼠标按下时的偏移量
x_offset = 0
y_offset = 0

# 为Label添加鼠标事件，用于拖动
time_label.bind("<ButtonPress-1>", on_press)
time_label.bind("<B1-Motion>", on_drag)

# 托盘图标右键菜单中的"退出"和"关于"选项
def on_quit(icon, item):
    icon.stop()
    root.quit()

def on_about(icon, item):
    # 显示关于信息框
    messagebox.showinfo("关于", "创作者：OvO\n版本：0.0.1")

def get_icon_image():
    if getattr(sys, 'frozen', False):  # 检查是否是打包后的exe文件
        icon_path = pkg_resources.resource_filename(
            __name__, 'time.ico')  # 访问打包在exe中的ico文件
    else:
        icon_path = "time.ico"  # 在开发过程中直接使用文件路径
    icon_image = Image.open(icon_path)
    return icon_image

# 创建托盘图标
def create_tray_icon():
    # 获取程序图标
    icon_handle = get_icon_image()  # 获取图标图像

    # 创建托盘菜单
    tray_menu = (
        item('关于', on_about),
        item('退出', on_quit)
    )

    # 创建托盘图标并启动
    icon = pystray.Icon("time_tray", icon_handle, title='桌面时钟正在运行' , menu=tray_menu)
    icon.run()

# 在单独的线程中运行托盘图标
tray_thread = threading.Thread(target=create_tray_icon)
tray_thread.daemon = True
tray_thread.start()

# 开始更新时间
update_time()

# 运行主循环
root.mainloop()
