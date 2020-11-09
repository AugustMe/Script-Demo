
# 参考：https://github.com/254675123/ai-video/blob/master/video_convertor/video_to_img.py
# https://github.com/254675123/ai-video/blob/master/video_convertor/video_image_convertor_2.py

# import cv2
#
# def video2image(video_filepath):
#     # 读入视频文件
#     vc = cv2.VideoCapture(video_filepath)
#     c = 0
#     rval = vc.isOpened()
#     # timeF = 1  #视频帧计数间隔频率
#     while rval:  # 循环读取视频帧
#         c = c + 1
#         rval, frame = vc.read()
#         #    if(c%timeF == 0): #每隔timeF帧进行存储操作
#         #        cv2.imwrite('smallVideo/smallVideo'+str(c) + '.jpg', frame) #存储为图像
#         if rval:
#             cv2.imwrite('img_res/' + str(c).zfill(8) + '.jpg', frame)  # 存储为图像
#             cv2.waitKey(1)
#         else:
#             break
#     vc.release()
#
# if __name__ == "__main__":
#     video2image("TomJerry.mp4")



import cv2
import os

def video2image(video_filepath):
    # 读入视频文件
    vc = cv2.VideoCapture(video_filepath)
    c = 0
    rval = vc.isOpened()
    timeF = 15 #视频帧计数间隔频率
    while rval:  # 循环读取视频帧
        c = c + 1
        rval, frame = vc.read()
        if(c%timeF == 0): #每隔timeF帧进行存储操作
            print("正在抽帧...... %d"%c)
            cv2.imwrite('img_res/'+str(c).zfill(6) + '.jpg', frame) #存储为图像
        # if rval:
        #     cv2.imwrite('img_res/' + str(c).zfill(6) + '.jpg', frame)  # 存储为图像
        #     cv2.waitKey(1)
        # else:
        #     break
    vc.release()

if __name__ == "__main__":
    if not os.path.exists("img_res"):
        os.mkdir("img_res")
    video2image("TomJerry.mp4")










