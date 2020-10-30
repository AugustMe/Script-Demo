# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 14:53:34 2020

@author: zqq

将一张图片填充为正方形后切为9张图
"""

from PIL import Image
import os

#将图片填充为正方形
def fill_image(image):
    width, height = image.size
    #选取长和宽中较大值作为新图片的
    new_image_length = width if width > height else height
    #生成新图片[白底]
    new_image = Image.new(image.mode, (new_image_length, new_image_length), color='white')
    #将之前的图粘贴在新图上，居中
    if width > height:#原图宽大于高，则填充图片的竖直维度
        #(x,y)二元组表示粘贴上图相对下图的起始位置
        new_image.paste(image, (0, int((new_image_length - height) / 2)))
    else: #原图宽<高，则填充图片的横向维度
        new_image.paste(image,(int((new_image_length - width) / 2),0))

    return new_image

### test fill_image()
# image_ori = Image.open("002.jpg")
# image_new = fill_image(image_ori)


#切图
def cut_image(image):
    width, height = image.size
    print("This pic (width, height):",width,height)
    item_width = int(width / 3)
    box_list = []
    # (left, upper, right, lower)
    for i in range(0,3):#两重循环，生成9张图片基于原图的位置
        for j in range(0,3):
            #print((i*item_width,j*item_width,(i+1)*item_width,(j+1)*item_width))
            box = (j*item_width,i*item_width,(j+1)*item_width,(i+1)*item_width)
            #print(box)
            box_list.append(box)

    image_list = [image.crop(box) for box in box_list]
    return image_list

### test cut_image()
# image_ori = Image.open("002.jpg")
# image_new = cut_image(image_ori)


#保存
def save_images(image_list):
    index = 1
    for image in image_list:
        if not os.path.exists('img_res'):
            os.mkdir('img_res')
        image.save('img_res/'+str(index) + '.png', 'PNG')
        index += 1

if __name__ == '__main__':
    file_path = "img/renwu.jpg"
    image = Image.open(file_path)
    #image.show()
    image = fill_image(image) # 填充
    image_list = cut_image(image)
    save_images(image_list)
