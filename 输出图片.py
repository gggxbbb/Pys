"""
实现控制台输出图片

依赖库:
    - Pillow
    - rich
    - numpy
"""

from PIL import Image

from rich.console import Console
from rich.text import Text
from rich.color import Color
from rich.style import Style

import numpy as np


def render_image(console: Console, image: Image.Image, texture: str = '▄') -> Text:
    """
    将 PIL.Image 对象转换为 rich.text.Text 对象，以便输出至 console
    :param texture: 像素材质
    :param console: 目标 console 对象
    :param image: 需要处理的 PIL.Image 对象
    :return: 可以直接输出的 rich.text.Text 对象
    """
    size = console.size
    width = int(size.width / 2)
    height = int(image.height * (width / image.width))
    image = image.resize((width, height))
    # noinspection PyTypeChecker
    pic = np.asarray(image)
    text = Text('', justify='center')
    for h in range(1, height, 2):
        for w in range(0, width):
            (r0, g0, b0) = pic[h - 1, w]
            (r, g, b) = pic[h, w]
            color = Color.from_rgb(r, g, b)
            bg_color = Color.from_rgb(r0, g0, b0)
            text.append(texture, style=Style(color=color, bgcolor=bg_color))
        text.append('\n')
    return text
