from cmath import sqrt
from turtle import width
import matplotlib.pyplot as plt

data = {
    "石蕊": [
        {
            "start": 0,
            "end": 4.5,
            "color": "red",
            "label": "红色"
        },
        {
            "start": 4.5,
            "end": 8.3,
            "color": "blueviolet",
            "label": "紫色"
        },
        {
            "start": 8.3,
            "end": 14.0,
            "color": "dodgerblue",
            "label": "蓝色"
        }
    ],
    "酚酞": [
        {
            "start": 0,
            "end": 8.2,
            "color": "white",
            "label": "无色"
        },
        {
            "start": 8.2,
            "end": 10.0,
            "color": "pink",
            "label": "浅红色"
        },
        {
            "start": 10.0,
            "end": 14.0,
            "color": "red",
            "label": "红色"
        }
    ],
    "甲基橙": [
        {
            "start": 0,
            "end": 3.1,
            "color": "red",
            "label": "红色"
        },
        {
            "start": 3.1,
            "end": 4.4,
            "color": "orange",
            "label": "橙色"
        },
        {
            "start": 4.4,
            "end": 14.0,
            "color": "yellow",
            "label": "黄色"
        }
    ],
    "甲基红": [
        {
            "start": 0,
            "end": 4.4,
            "color": "red",
            "label": "红色"
        },
        {
            "start": 4.4,
            "end": 6.2,
            "color": "orange",
            "label": "橙色"
        },
        {
            "start": 6.2,
            "end": 14.0,
            "color": "yellow",
            "label": "黄色"
        }
    ]
}

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.figsize'] = (16, 9)

plt.xlim(0, 14)
plt.ylim(0, len(data)+1)
plt.yticks(range(len(data)+1), [""]+list(data.keys()))
plt.gca().xaxis.set_major_locator(plt.MultipleLocator(0.5))
plt.title("高中常见酸碱指示剂")

drawed = []

for (k, v) in data.items():
    y = list(data.keys()).index(k)+1
    for i in v:
        plt.barh(y, i["end"] - i["start"], left=i["start"], height=0.7, color=i["color"], label=i["label"])
        if i["start"] != 0:
            plt.text(i["start"], y, i["start"], ha="center", va="center", fontsize=15)
            if not i["start"] in drawed:
                plt.axvline(i["start"], color="gray", linestyle="dotted", label=i["start"])
                drawed.append(i["start"])
        if i["end"] != 14:
            plt.text(i["end"], y, i["end"], ha="center", va="center", fontsize=15)
            if not i["end"] in drawed:
                plt.axvline(i["end"], color="gray", linestyle="dotted", label=i["end"])
                drawed.append(i["end"])
        x = i["start"] + (i["end"] - i["start"]) / 2
        plt.text(x, y, i["label"], ha="center", va="center")

plt.savefig(r"指示剂.svg")
plt.show()