import requests
import time

### 依赖
# requests

### 如何获取uuid
## 对于 Android 设备
## /storage/emulated/0/Android/data/com.alibaba.android.rimet/files/logs/trace/一串数字/live/最新的.log
## 搜索至最后一个 uuid= 到分号之前的一串就是uuid
## 对于 Windows 设备
## 不知道欸


uuid = input('uuid:')
c = 0

while True:
    try:
        re = requests.get(f'https://lv.dingtalk.com/interaction/createLike?uuid={uuid}&count=100')
    except KeyboardInterrupt:
        print(f'done {c}      ',end='\n')
    if 'success' in re.text:
        c += 1
        print(f'success*{c}',end='\r')
    else:
        print('\nerror')
    time.sleep(0.1)
