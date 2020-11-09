# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 08:28:00 2020

@author: zqq
"""

import cv2
def get_video_pic(name):
    cap = cv2.VideoCapture(name)
    time=cap.get(7)
    for i in range(0,int(time)):
            cap.set(1, int(i))
            print(cap.read())
            rval, frame = cap.read()
            if rval:
                cv2.imwrite('D:/kaobei/HyperLPR-master/HyperLPR-master/result'+str(i)+'.jpg', frame)#图片的路径
    cap.release()

get_video_pic("C:/Users/Lab/Desktop/4541.mp4")#视频的路径

