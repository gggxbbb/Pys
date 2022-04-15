import cv2
from PIL import Image
import numpy as np

from rich.console import Console
from rich.text import Text
from rich.color import Color
from rich.style import Style
from rich.live import Live

from datetime import datetime

cap = cv2.VideoCapture(r"Y:\OdEvax\班级杂物-下\2021市中运动会\🐟.mp4")
texture = '▄'

width0 = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height0 = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
total0 = cap.get(cv2.CAP_PROP_FRAME_COUNT)
fps0 = cap.get(cv2.CAP_PROP_FPS)

console = Console(color_system='truecolor', record=True)


width = int(console.size.width)
height = int(height0*(width/width0))

while width>console.size.width or height>console.size.height:
    width -= 1
    height = int(height0*(width/width0))
 
def build_frame(data, index, time, index2, time2):
    text = Text('frame %0.0f(%0.3f%%)/%0.0f time %0.2fs(%0.2fs)/%0.2fs \nfps %0.2f->%0.2f(average) %0.2f(3s)\n size %d*%d \n'%(
        index, index/total0*100, total0,
        index/fps0, time, total0/fps0,
        fps0, index/time, index2/time2,
        width, height
        ), 
        justify='center')
    im = Image.fromarray(data)
    im2 = im.resize((width, height))
    pic = np.asarray(im2)
    for h in range(1, height, 2):
        for w in range(0, width):
            (b0, g0, r0) = pic[h-1, w]
            (b, g, r) = pic[h, w]
            color = Color.from_rgb(r, g, b)
            bgcolor = Color.from_rgb(r0, g0, b0)
            text.append(texture, style=Style(color=color, bgcolor=bgcolor))
        text.append('\n')
    return text

success, cap1 = cap.read()

n = 1
n2 = 1

text1 = build_frame(cap1, n, 1, n2, 1)

start = datetime.now()
start2 = datetime.now()
with Live(text1, refresh_per_second=fps0, console=console) as live:
    while True:
        success, cap2 = cap.read()
        if not success:
            break
        n += 1
        n2 += 1
        now = datetime.now()
        text = build_frame(cap2, n, (now-start).total_seconds(), n2, (now-start2).total_seconds())
        if (now-start2).total_seconds()>3:
            start2 = now
            n2 = 1
        live.update(text)
    cap.release()
    live.stop()