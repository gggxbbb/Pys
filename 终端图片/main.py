from PIL import Image

from rich.console import Console
from rich.text import Text
from rich.color import Color
from rich.style import Style
from rich.markdown import Markdown

import numpy as np

texture = '▄'
msg = """# 测试图片

测试内容  
测试内容

1. 测试
2. 还是测试

[测试链接](https://www.baidu.com)

"""

md = Markdown(msg)

console = Console()

console.print(md)

size = console.size

im = Image.open('1.png')

width = int(size.width/2)
height = int(im.height*(width/im.width))

im2 = im.resize((width, height))

pic = np.asarray(im2)

opts = []

for h in range(1, height, 2):
    text = Text('')
    for w in range(0, width):
        (r0, g0, b0) = pic[h-1, w]
        (r, g, b) = pic[h, w]
        color = Color.from_rgb(r, g, b)
        bgcolor = Color.from_rgb(r0, g0, b0)
        text.append(texture, style=Style(color=color, bgcolor=bgcolor))

    opts.append(text)

for c in opts:
    console.print(c, justify='center')