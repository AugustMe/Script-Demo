# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 11:33:29 2021

@author: zqq
"""

from PIL import Image
import xml.etree.ElementTree as ET
import os


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



# 打开文件
classes = ["aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]

path_xml = "ds/xml"
path_pic = "ds/pic"
path_save = "ds_res/txt"
path_savepic = "ds_res/pic"
xml_dirs = os.listdir(path_xml)
# print(dirs)
# print(type(dirs))

# 遍历文件夹下所有xml
for file_xml in xml_dirs:
    # print(file_xml)
    txt_fpath = file_xml.split('.')[0] + '.txt'
    # print(txt_fpath)
    file_xml = os.path.join(path_xml,file_xml)
    txt_fpath = os.path.join(path_save,txt_fpath)
    # 调用 voc_xml_extract() 生成每个xml 对应 一个txt
    voc_xml_extract(file_xml, txt_fpath ,classes=classes)


# 遍历文件夹下所有txt
# 读取txt文件
path_txt = "ds_res/txt"
txt_dirs = os.listdir(path_txt)
# print(txt_dirs)

for file_txt in txt_dirs:
    # print(file_txt)
    with open( os.path.join(path_txt,file_txt), 'r' ) as f:
        lines = f.readlines()
        lines1 = [line.replace('\n','').split() for line in lines]
        lines2 = []
        for line in lines1:
            classname = classes[int(line[0])]
            # print(line[1:])
            xywh = [int(float(x)) for x in line[1:]]
            tem_res = [classname, xywh]
            lines2.append(tem_res)

    # img.crop
    # left：与左边界的距离
    # up：与上边界的距离
    # right：还是与左边界的距离
    # below：还是与上边界的距离
    # 简而言之就是，左上右下。
            
    pic_name =  file_txt.split('.')[0] + '.jpg'
    # print("pic_name:",pic_name)
    pic_fpath = os.path.join(path_pic,pic_name)
    # print("pic_fpath:",pic_fpath)
   
    print("pic_fpath:",pic_fpath)
    with open(pic_fpath, 'rb') as f:
        img = Image.open(f)
        for i in range(len(lines2)):
            img_crop = img.crop(lines2[i][1])
            # img_crop.save(lines2[i][0]+str(i) +'.jpg')
            img_crop.save(path_savepic +'/' + lines2[i][0]+ file_txt.split('.')[0]+'_' + str(i) +'.jpg')
