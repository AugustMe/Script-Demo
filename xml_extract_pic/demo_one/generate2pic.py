# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 10:53:07 2021

@author: zqq
"""

from PIL import Image

classes = ["aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]

# 读取txt文件
with open('000001.txt', 'r') as f:
    lines = f.readlines()
lines1 = [line.replace('\n','').split() for line in lines]
lines2 = []
for line in lines1:
    classname = classes[int(line[0])]
    print(line[1:])
    xywh = [int(float(x)) for x in line[1:]]
    tem_res = [classname, xywh]
    lines2.append(tem_res)

# img.crop
# left：与左边界的距离
# up：与上边界的距离
# right：还是与左边界的距离
# below：还是与上边界的距离
# 简而言之就是，左上右下。
with open('000001.jpg', 'rb') as f:
    img = Image.open(f)
    for i in range(len(lines2)):
        img_crop = img.crop(lines2[i][1])
        img_crop.save(lines2[i][0]+str(i) +'.jpg')
