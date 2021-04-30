# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 11:19:15 2021

@author: zqq
"""

from PIL import Image
import xml.etree.ElementTree as ET
import os
from os import listdir, getcwd
from os.path import join


classes = ['doubleskin']
# 读取xml文件
def voc_xml_extract(xml_fpath, txt_fpath, classes):
    # 一次读入xml的ElementTree
    with open(xml_fpath) as f:
        tree = ET.parse(f)
        root = tree.getroot()
        size = root.find('size')
        w = int(size.find('width').text)
        h = int(size.find('height').text)

    # 循环的将标记目标存入输出文件
    with open(txt_fpath, 'w') as f:
        for obj in root.iter('object'):
            difficult = obj.find('difficult').text
            clsname = obj.find('name').text
            if clsname not in classes or int(difficult) == 1:
                continue
            cls_id = classes.index(clsname)
            xmlbox = obj.find('bndbox')
            b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),float(xmlbox.find('ymax').text))
            bb = (b[0] ,b[2],b[1],b[3] )
            f.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
    return True 

voc_xml_extract('doubleskin_2020_26_33.xml', 'doubleskin_2020_26_33.txt' ,classes=classes)



# 读取txt文件
with open('doubleskin_2020_26_33.txt', 'r') as f:
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
with open('doubleskin_2020_26_33.jpg', 'rb') as f:
    img = Image.open(f)
    for i in range(len(lines2)):
        img_crop = img.crop(lines2[i][1])
        img_crop.save(lines2[i][0]+str(i) +'.jpg')




