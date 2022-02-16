import pyautogui
import win32api
import win32con
import time
import os
import sys

### 依赖
# pyautogui
# pywin32

### 用法
## 查找目标点
# python 点赞.py f
# 记录下目标点的坐标x,y
## 连点
# python 点赞.py r 刚刚的x 刚刚的y
# 鼠标移动至目标点附近自动点击， 10次/秒 

g_n = 0

def find():
    while True:
        x,y = pyautogui.position()
        print(f'Position: {x},{y}', end='         \r')

def good(g_x, g_y):
    global g_n
    n = 0
    while True:
        x,y = pyautogui.position()
        print(f'Position: {x},{y}', end=' ')
        if x in range(g_x-10,g_x+10) and y in range(g_y-10,g_y+10):
            print('Clicked', end=' ')
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0)
            n += 1
            g_n = n
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)
        else:
            print('Waiting', end=' ')
        print(n, end='           \r')
        time.sleep(0.1)

arg = sys.argv[1:]
if len(arg) == 0:
    print('参数错误')
elif arg[0] == 'f':
    try:
        find()
    except KeyboardInterrupt:
        x,y = pyautogui.position()
        print(f'Position: {x},{y}', end='\n')
elif arg[0] == 'r':
    try:
        good(int(arg[1]),int(arg[2]))
    except KeyboardInterrupt:
        x,y = pyautogui.position()
        print(f'Position: {x},{y} Done {g_n}      ',end='\n')
    except IndexError:
        print('参数错误')
    except ValueError:
        print('数据错误') 