# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 11:20:56 2020

@author: zqq
"""

import glob
import os
import cv2
import numpy as np

def put_image(input_path,output_path):
    imgs, heights, widths = [], [], [] # 定义三个空列表
    
    # 遍历读取方法 1：glob
    for f in glob.glob(input_path+"/"+"*.png"): # 遍历文件夹中的图片
    # for f in glob.glob("img/*.png") # 这种方法，也可以
        img = cv2.imread(f, -1)  # 参数-1表示返回原图
    
    # # 遍历读取方法 2: os.listdir()
    # for f in os.listdir(input_path):
    #     # print(f) # 图片名 1.png
    #     # print(input_path + "/" + f) # 路径 img/1.png
    #     img = cv2.imread(input_path + "/" + f)
        
        h, w = img.shape[:2]  # 切片
        heights.append(h)
        widths.append(w)
        imgs.append(img)
    
    min_height = min(heights)
    min_width = min(widths)
    for i, x in enumerate(imgs):
        # i为每个图像的序号, x为每个图像的多维像素矩阵
        imgs[i] = x[:min_height:3, :min_width:3]  # 切片 以步长为3
    
    img0 = np.concatenate(imgs[:3], 1)  # 横着拼三个
    img1 = np.concatenate(imgs[3:6], 1)  # 横着拼三个
    img2 = np.concatenate(imgs[6:], 1)  # 横着拼三个
    img9 = np.concatenate([img0, img1, img2], 0)  # 竖着拼起来
    cv2.imwrite(os.path.join(output_path,"result.jpg"), img9) # save
    
    
if __name__ == "__main__":
    input_path = "img"  # 存放九张图片的文件夹
    output_path= "img_res"  # 存放九合一的文件夹
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    put_image(input_path,output_path)
