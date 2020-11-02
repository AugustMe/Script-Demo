# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 11:24:48 2020

@author: zqq

linux环境下运行

"""

from PIL import Image
import glob
import os
from skimage import io

# 将图片填充为正方形
def fill_image(image):
    width, height = image.size
    # 选取长和宽中较大值作为新图片的
    new_image_length = width if width > height else height
    # 生成新图片[白底]
    new_image = Image.new(image.mode, (new_image_length, new_image_length), color='white')
    # 将之前的图粘贴在新图上，居中
    if width > height:  # 原图宽大于高，则填充图片的竖直维度
        # (x,y)二元组表示粘贴上图相对下图的起始位置
        new_image.paste(image, (0, int((new_image_length - height) / 2)))
    else:
        new_image.paste(image, (int((new_image_length - width) / 2), 0))
    return new_image

# 切图
def cut_image(image):
    width, height = image.size
    # print("iamge:", image.size)
    item_width = int(width / 3)
    item_height = int(height / 3)
    box_list = []
    # (left, upper, right, lower)
    for i in range(0, 3):  # 两重循环，生成9张图片基于原图的位置
        for j in range(0, 3):
            # print((i*item_width,j*item_width,(i+1)*item_width,(j+1)*item_width))
            box = (j * item_width, i * item_height, (j + 1) * item_width, (i + 1) * item_height)
            # print("box:", box)
            box_list.append(box)

    image_list = [image.crop(box) for box in box_list]
    return image_list
   
# 保存
def save_images(image_list,pic_id,folder):
    index = 1
    for image in image_list:
        # print("iamge type:", image)
        file_name = str(pic_id) + "_" + str(index) + '.jpg'  # png或者 jpg 都可以
        save_path = os.getcwd()+ '/img_res'+'/'+folder
        print('save_path:',save_path)
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        image.save( os.path.join(save_path,file_name) )

        index += 1
         
# 读取图片
def read_img(file_path):
    # data_list = [file_path + x for x in os.listdir(file_path) if os.path.isdir(file_path + x)] # 所有图片分类目录
    data_list = [x for x in os.listdir(file_path) if os.path.isdir(file_path)] # 所有图片分类目录
    print(data_list)
    for idx, folder in enumerate(data_list):  # 遍历每个文件夹中的图片，idx表示
        print(folder)
        for im in glob.glob(file_path+'/'+folder + '/*.jpg'):  # *:匹配0个或多个字符
            print('reading the images:%s' % (im))
            img = io.imread(im)
            img = Image.open(im)   
            #img.show()
            #img = fill_image(img) 
            image_list = cut_image(img) # 切图,对每张图片裁剪成9张
            # 获取图片id
            # print(im)
            pic_name = im.split('/')[-1] #取图片原名，去除图片名后缀
            pic_id = pic_name.split('.')[0]
            # print(pic_id)
            save_images(image_list,pic_id,folder) # 保存裁好的图片

# 运行接口
if __name__ == '__main__':            
    file_path = 'img'  # 路径
    read_img(file_path)
            
