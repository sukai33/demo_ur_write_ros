#!/usr/bin/env python
# coding:utf-8
from MainWindow import MainWindow
from PyQt5.QtWidgets import QApplication
import sys
from svg_class import *
import tensorflow as tf
from hsv_class import Hsv_change
import os
import cv2 as cv
import numpy as np
#from moviepy.editor import VideoFileClip
def t(img_path):
    """
    img转svg方法
    :param img_path: img路径
    :return: 返回output.svg绝对路径
    """
    os.system("convert " + img_path + " output_tmp.ppm")
    os.system("potrace output_tmp.ppm -b svg -u 1 --flat -o output.svg")
    os.system("rm output_tmp.ppm")
    return "{}/output.svg".format(os.popen("pwd").readline().rstrip('\r\n'))



i1 = 0
i2 = 0
i3 = 0
i4 = 0
i5 = 0
i6 = 0

def onChange(a,b,hsv):
    print(a)
    print(b)
    global i1,i2,i3,i4,i5,i6
    if a==1:
        i1 = b
    elif a==2:
        i2 = b
    elif a == 3:
        i3 = b
    elif a == 4:
        i4 = b
    elif a == 5:
        i5 = b
    elif a == 6:
        i6 = b
    lowerb = (i1, i2, i3)
    upperb = (i4, i5, i6)
    mask = cv.inRange(hsv, lowerb, upperb)
    cv.imshow("mask", mask)
    print(i1,i2,i3,i4,i5,i6)
    # lowerb_Parts = (154, 85, 79)
    # upperb_Parts = (195, 255, 255)


def inRange(dstImgggg):
    # img = cv2.imread("data2/test_aubo2.png")
    # img_copy=img.copy()
    img_copysize =cv.resize(dstImgggg,(int(dstImgggg.shape[1]/2),int(dstImgggg.shape[0]/2)))
    cv.imshow("img_copysize", img_copysize)
    hsv=cv.cvtColor(img_copysize,cv.COLOR_BGR2HSV)
    cv.imshow("hsv", hsv)
    cv.namedWindow("mask")
    cv.createTrackbar("h1", "mask", 0, 255, lambda a : onChange(1,a,hsv))
    cv.createTrackbar("s1", "mask", 0, 255, lambda a: onChange(2, a,hsv))
    cv.createTrackbar("v1", "mask", 0, 255, lambda a: onChange(3, a,hsv))
    cv.createTrackbar("h2", "mask", 0, 255, lambda a: onChange(4, a,hsv))
    cv.createTrackbar("s2", "mask", 0, 255, lambda a: onChange(5, a,hsv))
    cv.createTrackbar("v2", "mask", 0, 255, lambda a: onChange(6, a,hsv),)
    cv.waitKey(0)
    cv.destroyAllWindows()



def see_image_by_b5_new(dstImgggg):
# --------------测试预测数据------------------------
    #input_im=cv.imread("img/bbb.bmp")
    #gray=cv.cvtColor(input_im,cv.COLOR_BGR2GRAY)
    #print(gray.shape)
    hsv = cv.cvtColor(dstImgggg, cv.COLOR_BGR2HSV)
    lowerb = (0, 0, 113)
    upperb = (225, 255, 255)
    mask = cv.inRange(hsv, lowerb, upperb)
    mask = mask[143:405, 177:596]
    blurred=cv.GaussianBlur(mask,(5,5),0)
    edged=cv.Canny(blurred,30,150)
    cv.imshow("mask", mask)
    cv.imshow("edged", edged)
    _,contours,_ =  cv.findContours(edged.copy(),cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
        ## 基于外边框的坐标， 提取包裹数字的矩形
    for c in contours:
            (x, y, w, h) = cv.boundingRect(c)
            #把大小改成28*28
            mask = mask[y - 30:y + h + 10, x - 10:x + w + 10]
            cv.imshow("maskaa", mask)
            aa = cv.resize(mask, (28, 28))
            #把白底黑字 换成 黑底白字
            pre_image = 255 - aa
            cv.imshow("img", pre_image)
            model = tf.keras.models.load_model('h5/abc.h5')
            predict = model.predict(pre_image.reshape(1, 28, 28, 1))
            print(predict)
            ## 看哪个出现的次数最多。
            result = np.argmax(predict)
            print(result)
            cv.waitKey(0)
            cv.destroyAllWindows()

def aaa():
# --------------测试预测数据------------------------
    #input_im=cv.imread("img/bbb.bmp")
    #gray=cv.cvtColor(input_im,cv.COLOR_BGR2GRAY)
    #print(gray.shape)
    dstImgggg = cv.imread("img/tiger261.jpg")
    cv.imshow("dstImgggg", dstImgggg)
    hsv = cv.cvtColor(dstImgggg, cv.COLOR_BGR2HSV)
    lowerb = (0, 0, 113)
    upperb = (225, 255, 255)
    mask = cv.inRange(hsv, lowerb, upperb)
    print(mask.shape)
    cv.imshow("mask", mask)
    mask = mask[143:405, 177:596]
    # greeImg[int(rows / 2):rows, :] = 255
    #cv.imshow("mask1", mask)
    #aaa(mask)
    blurred=cv.GaussianBlur(mask,(5,5),0)
    edged=cv.Canny(blurred,30,150)
    cv.imshow("edged", edged)
    _,contours,_ =  cv.findContours(edged.copy(),cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
        ## 基于外边框的坐标， 提取包裹数字的矩形
    for c in contours:
            (x, y, w, h) = cv.boundingRect(c)
            cv.imshow("img111", mask[y-30 :y + h , x :x + w+10 ])
            cc = cv.resize(mask[y-30 :y + h , x :x + w ], (28, 28))
            cv.imshow("img1cc11", cc)
            #把大小改成28*28
            mask = mask[y - 10:y + h + 10, x - 10:x + w + 10]
            cv.imshow("maskaa", mask)
            aa = cv.resize(mask, (28, 28))
            #把白底黑字 换成 黑底白字
            pre_image = 255 - aa
            cv.imshow("img", pre_image)
            model = tf.keras.models.load_model('h5/abc.h5')
            predict = model.predict(pre_image.reshape(1, 28, 28, 1))
            print(predict)
            ## 看哪个出现的次数最多。
            result = np.argmax(predict)
            print(result)
            cv.waitKey(0)
            cv.destroyAllWindows()

def see_tensorflow_image():
    video = cv.VideoCapture(0)
    # 判断视频是否打开成功
    isOpened = video.isOpened()
    print("视频是否打开成功：", isOpened)
    # 获取图片的信息:帧率
    fps = video.get(cv.CAP_PROP_FPS)
    # 获取每帧宽度
    width = video.get(cv.CAP_PROP_FRAME_WIDTH)
    # 获取每帧的高度
    height = video.get(cv.CAP_PROP_FRAME_HEIGHT)
    print("帧率：{},宽度：{},高度：{}".format(fps, width, height))

    # 从视频中读取8帧信息
    count = 0

    while True:
        count = count + 1
        # 读取成功or失败， 当前帧数据
        flag, frame = video.read()
        # frame=cv.flip(frame, 1) #镜像

        kernel = cv.getStructuringElement(cv.MORPH_RECT, (10, 10));
        # 膨胀
        # dst = cv.dilate(frame,kernel)
        dst = cv.erode(frame, kernel)
        # cv.imshow("dst",dst)
        # cv.imshow("src",frame)

        #cv.imshow("frame1", dst);  # 显示视频
        #see_image_by_b5(dst)
        action = cv.waitKey(100) & 0xFF
        ACTION_ESC = 27;
        ACTION_SPACE = 32;
        getMask(dst)

        #see_image_by_b5(dst)
        if (action == ACTION_SPACE or action == 'q'):
            cv.imwrite("img/tiger%d.jpg" % count, dst, [cv.IMWRITE_JPEG_QUALITY, 100])
            #aaa(dst )
            see_image_by_b5_new(dst)
            return -1
        if (action == ACTION_ESC):
           return -1

        # 将图片信息写入到文件中
        if flag:  # 保存
            # 图片的质量
            # cv.imwrite("img/tiger%d.jpg"%count,frame,[cv.IMWRITE_JPEG_QUALITY,100])
            pass
    print("图片截取完成啦！")
    cv.waitKey(0)
    cv.destroyAllWindows()

##看获取的数据
def getMask(dstImgggg):
    hsv = cv.cvtColor(dstImgggg, cv.COLOR_BGR2HSV)
    lowerb = (0, 0, 113)
    upperb = (225, 255, 255)
    mask = cv.inRange(hsv, lowerb, upperb)
    print(mask.shape)

    mask = mask[143:405, 177:596]
    blurred = cv.GaussianBlur(mask, (5, 5), 0)
    edged = cv.Canny(blurred, 30, 150)
    cv.imshow("mask", mask)


def see_image_by_b5(dstImgggg):
# --------------测试预测数据------------------------
    #input_im=cv.imread("img/bbb.bmp")
    #gray=cv.cvtColor(input_im,cv.COLOR_BGR2GRAY)
    #print(gray.shape)
    hsv = cv.cvtColor(dstImgggg, cv.COLOR_BGR2HSV)
    lowerb = (0, 0, 113)
    upperb = (225, 255, 255)
    mask = cv.inRange(hsv, lowerb, upperb)
    mask = mask[143:405, 177:596]
    blurred=cv.GaussianBlur(mask,(5,5),0)
    edged=cv.Canny(blurred,30,150)
    cv.imshow("mask1", mask)
    #cv.imshow("edged", edged)
    _,contours,_ =  cv.findContours(edged.copy(),cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
        ## 基于外边框的坐标， 提取包裹数字的矩形
    for c in contours:
        (x, y, w, h) = cv.boundingRect(c)
        # 把大小改成28*28
        mask = mask[y - 30:y + h + 10, x - 10:x + w + 10]
        #cv.imshow("maskaa", mask)
        aa = cv.resize(mask, (28, 28))
        # 把白底黑字 换成 黑底白字
        #pre_image = 255 - aa
        #cv.imshow("img", pre_image)
        #cv.waitKey(10)


    cv.imshow("maskaa", edged)
    #aa = cv.resize(mask, (28, 28))
    #pre_image = 255 - aa
    #action =cv.waitKey(0)
    ACTION_ESC = 27;
    ACTION_SPACE = 32;
    #if (action == ACTION_SPACE or action == 'q'):
       # model = tf.keras.models.load_model('h5/abc.h5')
        #predict = model.predict(pre_image.reshape(1, 28, 28, 1))
        # print(predict)
        #     ## 看哪个出现的次数最多。
        # result = np.argmax(predict)
        #print(result)


            #cv.destroyAllWindows()




def start():
    '''
       开始
       :return:
    '''
    ##svg数据
    # svg=svgPain()
    # svg.paintEvent()
    #--------------手写qt------------------------

    #创建程序
    app = QApplication(sys.argv)
    # 创建窗口
    window = MainWindow()
    # 显示窗口
    window.show()
    # 等待窗口关闭
    sys.exit(app.exec_())

    # --------------测试预测数据------------------------
    # input_im=cv.imread("img/bbb.bmp")
    # gray=cv.cvtColor(input_im,cv.COLOR_BGR2GRAY)
    # blurred=cv.GaussianBlur(gray,(5,5),0)
    # edged=cv.Canny(blurred,30,150)
    # _,contours,_ =  cv.findContours(edged.copy(),cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    #     ## 基于外边框的坐标， 提取包裹数字的矩形
    # for c in contours:
    #         (x, y, w, h) = cv.boundingRect(c)
    #         # 把大小改成28*28
    #         aa = cv.resize(gray[y - 10:y + h + 10, x - 10:x + w + 10], (28, 28))
    #         # 把白底黑字 换成 黑底白字
    #         pre_image = 255 - aa
    #         cv.imshow("img", pre_image)
    #         print(pre_image.shape)
    #         model = tf.keras.models.load_model('h5/abc.h5')
    #         predict = model.predict(pre_image.reshape(1, 28, 28, 1))
    #         print(predict)
    #         ## 看哪个出现的次数最多。
    #         result = np.argmax(predict)
    #         print(result)
    #         cv.waitKey(0)
    #         cv.destroyAllWindows()


    #see_tensorflow_image()
    #aaa()



if __name__ == '__main__':
    #0 0 113 255 255 255
    #   x 148 539   y 139 390
    #dstImgggg=cv.imread("img/tiger261.jpg")
    #inRange(dstImgggg)
    #h=Hsv_change()
    #h.inRange_byFilePath()
    start()
    #t("img/aaa.bmp")
    # st='28.000000pt'
    # print(st.find("."))
    # print(st[:st.find(".")])


