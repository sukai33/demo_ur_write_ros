#!/usr/bin/env python
# coding:utf-8
# 读取svg的xml文件
from xml.dom import minidom
# 解析svg路径
from svg.path import parse_path
import numpy as np
import cv2 as cv
import random
from locals import *
import tensorflow as tf
import os

class svgPain:

    def __init__(self,filepath='svg/8.svg'):


        self.RED = (0, 0, 255)
        # 定义列表 保存所有的path的d属性 pip3  install svg.path
        #self.pathsList = []
        self.points = []


        # ------------------------- 绘制 -------------------------#
        #空画布
        self.dst = np.zeros((640, 480, 3), dtype=np.uint8)
        #位移
        self.translate = "0"
        #缩放
        self.scales = "0"
        pass

    # 随机颜色
    def randomColor(self):
        return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

    # ------------------------- 绘制move down-------------------------#
    def drawMove(self,ele):
        start = int(ele.start.real), int(ele.start.imag)
        ##图像显示
        # cv.line(self.dst, start, start, self.randomColor())
        # cv.imshow('dst', self.dst)
        # cv.waitKey(5)
        z = 30.25
        # 创建点
        point = {'x': start[0], 'y': start[1], 'z': z, 'type': TYPE.DOWN, 'type2': 'drawMoveStart'}
        # 添加到容器中
        self.points.append(point)

    # ------------------------- 绘制直线 -------------------------#
    # Line(start=(424.81453999999997+371.04679000000004j), end=(424.81453999999997+369.04679000000004j))
    def drawLine(self,ele):
        start = int(ele.start.real), int(ele.start.imag)
        end = int(ele.end.real), int(ele.end.imag)
        # cv.line(self.dst, start, end, self.RED)
        # cv.imshow('dst', self.dst)
        # cv.waitKey(5)
        z = 30.25
        # 创建点
        point = {'x': start[0], 'y': start[1], 'z': z, 'type': TYPE.MOVE, 'type2': 'drawLineStart'}
        # 添加到容器中
        self.points.append(point)
        point = {'x': end[0], 'y': end[1], 'z': z, 'type': TYPE.MOVE,'type2': 'drawLineEnd'}
        # 添加到容器中
        self.points.append(point)

    # ------------------------- 绘制二阶贝塞尔 -------------------------#
    def QuadraticBezier(self,ps, pc, pe, t):
        '''
        获取二阶贝塞尔点
        :param ps: 开始点
        :param pc: 控制点
        :param pe: 结束点
        :param t: 0-1
        :return:
        '''
        return pow(1 - t, 2) * ps + 2 * t * (1 - t) * pc + pow(t, 2) * pe

    def drawQuadraticBezier(self,ele):
        # 开始点
        ps = np.array([ele.start.real, ele.start.imag])
        # 控制点
        p = np.array([ele.control.real, ele.control.imag])
        # 结束点
        pe = np.array([ele.end.real, ele.end.imag])
        point = self.QuadraticBezier(ps, p, pe, 0)
        start = int(point[0]), int(point[1])
        z = 30.25
        # 创建点
        point = {'x': start[0], 'y': start[1], 'z': z, 'type': TYPE.MOVE, 'type2': 'drawQuadraticBezierStart'}
        # 添加到容器中
        self.points.append(point)
        # 40个点
        for i in range(1, 41):
            result = self.QuadraticBezier(ps, p, pe, i / 40)
            end = int(result[0]), int(result[1])
            # 创建点
            point = {'x': end[0], 'y': end[1], 'z': z, 'type': TYPE.MOVE, 'type2': 'drawQuadraticBezierEnd'}
            # 添加到容器中
            self.points.append(point)
            # 连接两个点
            # cv.line(self.dst, start, end, self.randomColor())
            # cv.imshow('dst', self.dst)
            # cv.waitKey(5)
            # 开始点变成结束点
            #start = end

    # ------------------------- 三阶贝塞尔 -------------------------#
    def CubicBezier(self,ps, pc1, pc2, pe, t):
        '''
        获取二阶贝塞尔点
        :param ps: 开始点
        :param pc: 控制点
        :param pe: 结束点
        :param t: 0-1
        :return:
        '''
        return pow(1 - t, 3) * ps + 3 * t * pow(1 - t, 2) * pc1 + 3 * pow(t, 2) * (1 - t) * pc2 + pow(t, 3) * pe

    def drawCubicBezier(self,ele):
        print('绘制贝塞尔')
        # 开始点
        ps = np.array([ele.start.real, ele.start.imag])
        # 控制点
        p1 = np.array([ele.control1.real, ele.control1.imag])
        p2 = np.array([ele.control2.real, ele.control2.imag])
        # 结束点
        pe = np.array([ele.end.real, ele.end.imag])
        result = self.CubicBezier(ps, p1, p2, pe, 0)
        print(result)
        start = int(result[0]), int(result[1])
        z = 30.25
        # 创建点
        point = {'x': start[0], 'y': start[1], 'z': z, 'type': TYPE.MOVE, 'type2': 'drawCubicBezierStart'}
        # 添加到容器中
        self.points.append(point)
        # 40个点
        for i in range(1, 41):
            result = self.CubicBezier(ps, p1, p2, pe, i / 40)
            end = int(result[0]), int(result[1])
            # 创建点
            point = {'x': end[0], 'y': end[1], 'z': z, 'type': TYPE.MOVE, 'type2': 'drawCubicBezierEnd'}
            # 添加到容器中
            self.points.append(point)
            # 连接两个点
            # cv.line(self.dst, start, end, self.randomColor())
            # cv.imshow('dst', self.dst)
            # cv.waitKey(5)
            # # 开始点变成结束点
            # start = end

    # ------------------------- 结束点 -------------------------#
    def drawClose(self,ele):
        z = 30.25
        start = int(ele.start.real), int(ele.start.imag)
        # 创建点
        # point = {'x': x, 'y': y, 'type': TYPE.UP}
        point = {'x': start[0], 'y': start[1], 'z': z, 'type': TYPE.MOVE, 'type2': 'drawCloseStart'}
        # 添加到容器中
        self.points.append(point)
        end = int(ele.end.real), int(ele.end.imag)
        z = 45.55
        point = {'x': end[0], 'y': end[1], 'z': z, 'type': TYPE.UP,  'type2': 'drawCloseEnd'}
        # 添加到容器中
        self.points.append(point)

        # cv.line(self.dst, start, end, self.randomColor())
        # cv.imshow('dst', self.dst)
        # cv.waitKey(5)

    def paintEvent(self,filepath='svg/8.svg'):
        #"img/output.svg"
        #'svg/8.svg'
        #filepath = 'svg/8.svg'
        #filepath = 'svg/che.svg'
        filepath = 'img/output.svg'
        #filepath = 'svg/5.svg'
        # 1.读取xml文件
        doc = minidom.parse(filepath)
        # 2.查找path标签
        paths = doc.getElementsByTagName('path')
        svgTag = doc.getElementsByTagName('svg')
        self.w = svgTag[0].getAttribute('width')
        self.h = svgTag[0].getAttribute('height')

        ##获取位移与缩放比例
        gs = doc.getElementsByTagName('g')

        translates_scales = gs[0].getAttribute('transform').split(" ")
        if len(translates_scales) > 1:
            translates, scales = translates_scales
            print(translates.find("("))
            print(scales.find("("))
            # 位移
            self.translate = translates[translates.find("(") + 1:len(translates) - 1].split(',')
            # 缩放比例
            self.scales = scales[scales.find("(") + 1:len(scales) - 1].split(',')

        print(self.w, self.h)
        pathsList = []
        for path in paths:
            pathsList.append(path.getAttribute('d'))
        # 解析路径字符串
        for path in pathsList:
            result = parse_path(path)
            # path  序列  可以通过for循环获取所有的元素
            for ele in result:
                print(type(ele).__name__)
                if type(ele).__name__ == 'Move':
                    self.drawMove(ele)
                elif type(ele).__name__ == 'Line':
                    self.drawLine(ele)
                elif type(ele).__name__ == 'CubicBezier':
                    self.drawCubicBezier(ele)
                elif type(ele).__name__ == 'QuadraticBezier':
                    self.drawQuadraticBezier(ele)
                elif type(ele).__name__ == 'Close':
                    self.drawClose(ele)
                else:
                    print('其他')

        #cv.waitKey(0)

    # 识别图片写字
    def tensorflow_see(self,input_im):
        model = tf.keras.models.load_model('h5/abc.h5')
        predict = model.predict(input_im.reshape(1,28,28,1))
        self.result = np.argmax(predict)


    # 识别图片写字
    def image_word(self,input_im):
        gray=cv.cvtColor(input_im,cv.COLOR_BGR2GRAY)
        blurred=cv.GaussianBlur(gray,(5,5),0)
        edged=cv.Canny(blurred,30,150)
        _,contours,_ =  cv.findContours(edged.copy(),cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
        ## 基于外边框的坐标， 提取包裹数字的矩形
        for c in contours:
            area = cv.contourArea(c)
            print("area1: ".format(area))
            (x, y, w, h) = cv.boundingRect(c)
            # 把大小改成28*28
            gray=gray[y - 10:y + h + 10, x - 10:x + w + 10]
            aa = cv.resize(gray, (28, 28))
            # 把白底黑字 换成 黑底白字
            pre_image = 255 - aa
            self.tensorflow_see(pre_image)
            # cv.imshow("img", pre_image)
            # cv.waitKey(0)
            # cv.destroyAllWindows()
    #识别图片写字
    def paintEvent_byImage(self, input_im):
        self.image_word(input_im)
        print(self.result)
        filepath1="img/{}.svg".format(self.result)
        # 1.读取xml文件
        doc = minidom.parse(filepath1)
        # 2.查找path标签
        paths = doc.getElementsByTagName('path')
        svgTag = doc.getElementsByTagName('svg')
        self.w = svgTag[0].getAttribute('width')
        self.h = svgTag[0].getAttribute('height')
        print(self.w, self.h)
        pathsList = []
        for path in paths:
            pathsList.append(path.getAttribute('d'))
        # 解析路径字符串
        for path in pathsList:
            result = parse_path(path)
            # path  序列  可以通过for循环获取所有的元素
            for ele in result:
                print(type(ele).__name__)
                if type(ele).__name__ == 'Move':
                    self.drawMove(ele)
                elif type(ele).__name__ == 'Line':
                    self.drawLine(ele)
                elif type(ele).__name__ == 'CubicBezier':
                    self.drawCubicBezier(ele)
                elif type(ele).__name__ == 'QuadraticBezier':
                    self.drawQuadraticBezier(ele)
                elif type(ele).__name__ == 'Close':
                    self.drawClose(ele)
                else:
                    print('其他')

    # 通过摄像头识别写标准字
    def paintEvent_byVideo(self, result):
        filepath1 = "img/{}.svg".format(result)
        # 1.读取xml文件
        doc = minidom.parse(filepath1)
        # 2.查找path标签
        paths = doc.getElementsByTagName('path')
        svgTag = doc.getElementsByTagName('svg')
        self.w = svgTag[0].getAttribute('width')
        self.h = svgTag[0].getAttribute('height')
        print(self.w, self.h)
        pathsList = []
        for path in paths:
            pathsList.append(path.getAttribute('d'))
        # 解析路径字符串
        for path in pathsList:
            result = parse_path(path)
            # path  序列  可以通过for循环获取所有的元素
            for ele in result:
                print(type(ele).__name__)
                if type(ele).__name__ == 'Move':
                    self.drawMove(ele)
                elif type(ele).__name__ == 'Line':
                    self.drawLine(ele)
                elif type(ele).__name__ == 'CubicBezier':
                    self.drawCubicBezier(ele)
                elif type(ele).__name__ == 'QuadraticBezier':
                    self.drawQuadraticBezier(ele)
                elif type(ele).__name__ == 'Close':
                    self.drawClose(ele)
                else:
                    print('其他')

    ##通过摄像头识别图像 空格键获取 入口
    def see_tensorflow_Video(self):
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

            cv.imshow("frame1", dst);  # 显示视频
            action = cv.waitKey(120) & 0xFF
            ACTION_ESC = 27
            ACTION_SPACE = 32
            self.getMask_Video(dst)
            if (action == ACTION_SPACE or action == 'q'):
                # cv.imwrite("img/tiger%d.jpg" % count, dst, [cv.IMWRITE_JPEG_QUALITY, 100])
                # aaa(dst )
                self.see_image_by_b5_Video(dst)
                # cv.imwrite("img/tiger%d.jpg" % count, dst, [cv.IMWRITE_JPEG_QUALITY, 100])
                return -1
            if (action == ACTION_ESC):
                return -1

            # 将图片信息写入到文件中
            if flag:  # 保存
                # 图片的质量
                # cv.imwrite("img/tiger%d.jpg"%count,frame,[cv.IMWRITE_JPEG_QUALITY,100])
                pass
        print("图片截取完成啦！")
        # cv.waitKey(0)
        cv.destroyAllWindows()

    ##看获取的数据
    def getMask_Video(self,dstImgggg):
        hsv = cv.cvtColor(dstImgggg, cv.COLOR_BGR2HSV)
        lowerb = (0, 0, 113)
        upperb = (225, 255, 255)
        mask = cv.inRange(hsv, lowerb, upperb)
        mask = mask[143:405, 177:596]
        blurred = cv.GaussianBlur(mask, (5, 5), 0)
        edged = cv.Canny(blurred, 30, 150)
        cv.imshow("mask", mask)

    def see_image_by_b5_Video(self,dstImgggg):
        # --------------测试预测数据------------------------
        # input_im=cv.imread("img/bbb.bmp")
        # gray=cv.cvtColor(input_im,cv.COLOR_BGR2GRAY)
        # print(gray.shape)
        hsv = cv.cvtColor(dstImgggg, cv.COLOR_BGR2HSV)
        lowerb = (0, 0, 113)
        upperb = (225, 255, 255)
        mask = cv.inRange(hsv, lowerb, upperb)
        mask = mask[143:405, 177:596]
        blurred = cv.GaussianBlur(mask, (5, 5), 0)
        edged = cv.Canny(blurred, 30, 150)
        cv.imshow("mask", mask)
        cv.imshow("edged", edged)
        _, contours, _ = cv.findContours(edged.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        ## 基于外边框的坐标， 提取包裹数字的矩形
        for c in contours:
            area = cv.contourArea(c)
            print("area: ".format(area))
            (x, y, w, h) = cv.boundingRect(c)
            # 把大小改成28*28
            mask = mask[y - 10:y + h + 10, x - 10:x + w + 10]
            cv.imshow("maskaa", mask)
            aa = cv.resize(mask, (28, 28))
            # 把白底黑字 换成 黑底白字
            pre_image = 255 - aa
            cv.imshow("img", pre_image)
            print(pre_image.shape)
            model = tf.keras.models.load_model('h5/abc.h5')
            predict = model.predict(pre_image.reshape(1, 28, 28, 1))
            print(predict)
            ## 看哪个出现的次数最多。
            result = np.argmax(predict)
            print(result)
            self.paintEvent_byVideo(result)
            cv.waitKey(500)
            return
            cv.waitKey(0)
            #cv.destroyAllWindows()

        ## 通过摄像头识别图像,通过 空格键获取图片 入口
    def see_tensorflow_Video_getimage(self):
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
                flag, dst = video.read()
                # frame=cv.flip(frame, 1) #镜像

                kernel = cv.getStructuringElement(cv.MORPH_RECT, (10, 10));
                # 膨胀
                # dst = cv.dilate(frame,kernel)
                #dst = cv.erode(frame, kernel)
                # cv.imshow("dst",dst)
                # cv.imshow("src",frame)

                cv.imshow("frame1", dst);  # 显示视频
                action = cv.waitKey(120) & 0xFF
                ACTION_ESC = 27;
                ACTION_SPACE = 32;
                self.getMask_Video(dst)
                if (action == ACTION_SPACE or action == 'q'):
                    # cv.imwrite("img/tiger%d.jpg" % count, dst, [cv.IMWRITE_JPEG_QUALITY, 100])
                    # aaa(dst )
                    self.see_image_by_Video_getimage(dst)

                    return -1
                if (action == ACTION_ESC):
                    return -1

            # cv.waitKey(0)
            cv.destroyAllWindows()

    def imgTosvg(self,img_path):
        """
            img转svg方法
            :param img_path: img路径
            :return: 返回output.svg绝对路径
            """
        os.system("convert " + img_path + " output_tmp.ppm")
        os.system("potrace output_tmp.ppm -b svg -u 1 --flat -o img/output.svg")
        os.system("rm output_tmp.ppm")
        #os.system("rm {}/img/output.jpg".format(os.popen("pwd").readline().rstrip('\r\n')))
        print( "{}/img/output.svg".format(os.popen("pwd").readline().rstrip('\r\n')))
        self.paintEvent("img/output.svg")
        pass

    # 通过摄像头识别图像,通过 空格键获取图片 入口
    def see_image_by_Video_getimage(self,dstImgggg):
        # --------------测试预测数据------------------------
        hsv = cv.cvtColor(dstImgggg, cv.COLOR_BGR2HSV)
        lowerb = (0, 0, 113)
        upperb = (225, 255, 255)
        mask = cv.inRange(hsv, lowerb, upperb)
        mask = mask[143:405, 177:596]
        blurred = cv.GaussianBlur(mask, (5, 5), 0)
        edged = cv.Canny(blurred, 30, 150)
        cv.imshow("mask", mask)
        cv.imshow("edged", edged)
        _, contours, _ = cv.findContours(edged.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        ## 基于外边框的坐标， 提取包裹数字的矩形
        for c in contours:
            area = cv.contourArea(c)
            print("area: ".format(area))
            (x, y, w, h) = cv.boundingRect(c)
            # 把大小改成28*28
            mask = mask[y - 10:y + h + 10, x - 10:x + w + 10]
            cv.imshow("maskaa", mask)
            cv.imwrite("img/output.jpg", mask, [cv.IMWRITE_JPEG_QUALITY, 100])
            self.imgTosvg("img/output.jpg")
            cv.waitKey(500)
            return
            cv.waitKey(0)
            #cv.destroyAllWindows()

