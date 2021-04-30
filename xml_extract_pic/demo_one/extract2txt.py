# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 10:43:09 2021

@author: zqq
"""

import xml.etree.ElementTree as ET


# 读取xml文件
def voc_xml_extract(xml_fpath, txt_fpath, classes):
    # 一次读入xml的ElementTree
    with open(xml_fpath) as f:
        tree = ET.parse(f)
        root = tree.getroot()
        # size = root.find('size')
        # w = int(size.find('width').text)
        # h = int(size.find('height').text)

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


classes = ["aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]
voc_xml_extract('000001.xml', '000001.txt' ,classes=classes)
