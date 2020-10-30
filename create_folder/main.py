# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 10:56:56 2020

@author: zqq
"""
import os 
import shutil

def create_folder_pic(read_path,save_path):
    for picname in os.listdir(read_path):
        #print(picname)
        foldername = picname[:14]
        # 创建文件夹
        if not os.path.exists(os.path.join(save_path,foldername)):
            os.makedirs(os.path.join(save_path,foldername))
            print("%s folder create sucess!" % os.path.join(save_path,foldername))
        for foldername in os.listdir(save_path):
            #print(foldername)
            if foldername == picname[:14]:
                print('%s Transfer sucess!'%picname)
                # copy复制，move移动
                shutil.copy(os.path.join(read_path,picname),os.path.join(save_path,foldername))
                # shutil.move(os.path.join(read_path,picname),os.path.join(save_path,foldername))

if __name__ =="__main__":
    # 读取图片的路径
    read_path = r"C:\Users\zqq\Desktop\test\FGpic"
    # 保存图片路径 
    save_path = "Result"
    create_folder_pic(read_path,save_path) # 调用函数
    