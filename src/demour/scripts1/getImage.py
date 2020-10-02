#!/usr/bin/env python
# coding:utf-8

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import tensorflow as tf
import cv2 as cv
import numpy as np
from std_msgs.msg import String
from diagnostic_msgs.msg import DiagnosticArray
from diagnostic_msgs.msg import DiagnosticStatus
from diagnostic_msgs.msg import KeyValue
from xml.dom import minidom
import random
# 解析svg路径  minidom报错没关系
from svg.path import parse_path
import os
 ##diagnostic_msgs/KeyValue
 ##diagnostic_msgs/DiagnosticArray

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
    def drawMove(self,ele,da):
        start = int(ele.start.real), int(ele.start.imag)
        ##图像显示
        # cv.line(self.dst, start, start, self.randomColor())
        # cv.imshow('dst', self.dst)
        # cv.waitKey(5)
        z = 30.25
        # 创建点
        point = {'x': str(start[0]), 'y': str(start[1]), 'z': str(z), 'type': 'DOWN', 'type2': 'drawMoveStart'}
        points=DiagnosticStatus()
        points.values.append(KeyValue('x',str(start[0])))

        points.values.append(KeyValue('y',str(start[1])))

        points.values.append(KeyValue('z',str(z)))

        points.values.append(KeyValue('type','DOWN'))

        points.values.append(KeyValue('type2','drawMoveStart'))
        da.status.append(points)
        # 添加到容器中
        self.points.append(point)

    # ------------------------- 绘制直线 -------------------------#
    # Line(start=(424.81453999999997+371.04679000000004j), end=(424.81453999999997+369.04679000000004j))
    def drawLine(self,ele,da):
        start = int(ele.start.real), int(ele.start.imag)
        end = int(ele.end.real), int(ele.end.imag)
        # cv.line(self.dst, start, end, self.RED)
        # cv.imshow('dst', self.dst)
        # cv.waitKey(5)
        z = 30.25
        # 创建点
        point = {'x': str(start[0]), 'y': str(start[1]), 'z': str(z), 'type': 'MOVE', 'type2': 'drawLineStart'}

        points=DiagnosticStatus()
        points.values.append(KeyValue('x',str(start[0])))

        points.values.append(KeyValue('y',str(start[1])))

        points.values.append(KeyValue('z',str(z)))

        points.values.append(KeyValue('type','MOVE'))

        points.values.append(KeyValue('type2','drawLineStart'))
        da.status.append(points)
        # 添加到容器中
        self.points.append(point)
        point = {'x': str(end[0]), 'y': str(end[1]), 'z': str(z), 'type': 'MOVE','type2': 'drawLineEnd'}
        points=DiagnosticStatus()
        points.values.append(KeyValue('x',str(end[0])))

        points.values.append(KeyValue('y',str(end[1])))

        points.values.append(KeyValue('z',str(z)))

        points.values.append(KeyValue('type','MOVE'))

        points.values.append(KeyValue('type2','drawLineEnd'))
        da.status.append(points)
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

    def drawQuadraticBezier(self,ele,da):
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
        point = {'x': str(start[0]), 'y': str(start[1]), 'z': str(z), 'type': 'MOVE', 'type2': 'drawQuadraticBezierStart'}

        points=DiagnosticStatus()
        points.values.append(KeyValue('x',str(start[0])))

        points.values.append(KeyValue('y',str(start[1])))

        points.values.append(KeyValue('z',str(z)))

        points.values.append(KeyValue('type','MOVE'))

        points.values.append(KeyValue('type2','drawQuadraticBezierStart'))
        da.status.append(points)
        # 添加到容器中
        self.points.append(point)
        # 40个点
        for i in range(1, 41):
            result = self.QuadraticBezier(ps, p, pe, i / 40)
            end = int(result[0]), int(result[1])
            # 创建点

            point = {'x': str(end[0]), 'y': str(end[1]), 'z': str(z), 'type': 'MOVE', 'type2': 'drawQuadraticBezierEnd'}
            points=DiagnosticStatus()
            points.values.append(KeyValue('x',str(end[0])))

            points.values.append(KeyValue('y',str(end[1])))

            points.values.append(KeyValue('z',str(z)))

            points.values.append(KeyValue('type','MOVE'))

            points.values.append(KeyValue('type2','drawQuadraticBezierEnd'))
            da.status.append(points)

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

    def drawCubicBezier(self,ele,da):
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
        point = {'x': str(start[0]), 'y': str(start[1]), 'z': str(z), 'type': 'MOVE', 'type2': 'drawCubicBezierStart'}

        points=DiagnosticStatus()
        points.values.append(KeyValue('x',str(start[0])))

        points.values.append(KeyValue('y',str(start[1])))

        points.values.append(KeyValue('z',str(z)))

        points.values.append(KeyValue('type','MOVE'))

        points.values.append(KeyValue('type2','drawCubicBezierStart'))
        da.status.append(points)
        # 添加到容器中
        self.points.append(point)
        # 40个点
        for i in range(1, 41):
            result = self.CubicBezier(ps, p1, p2, pe, i / 40)
            end = int(result[0]), int(result[1])
            # 创建点
            point = {'x': str(end[0]), 'y': str(end[1]), 'z': str(z), 'type': 'MOVE', 'type2': 'drawCubicBezierEnd'}

            points=DiagnosticStatus()
            points.values.append(KeyValue('x',str(end[0])))

            points.values.append(KeyValue('y',str(end[1])))

            points.values.append(KeyValue('z',str(z)))

            points.values.append(KeyValue('type','MOVE'))

            points.values.append(KeyValue('type2','drawCubicBezierEnd'))
            da.status.append(points)

            # 添加到容器中
            self.points.append(point)
            # 连接两个点
            # cv.line(self.dst, start, end, self.randomColor())
            # cv.imshow('dst', self.dst)
            # cv.waitKey(5)
            # # 开始点变成结束点
            # start = end

    # DOWN = 0
    # MOVE = 1
    # UP = 2

    # ------------------------- 结束点 -------------------------#
    def drawClose(self,ele,da):
        z = 30.25
        start = int(ele.start.real), int(ele.start.imag)
        # 创建点
        # point = {'x': x, 'y': y, 'type': TYPE.UP}
        point = {'x': str(start[0]), 'y': str(start[1]), 'z': str(z), 'type': 'MOVE', 'type2': 'drawCloseStart'}
        points=DiagnosticStatus()
        points.values.append(KeyValue('x',str(start[0])))

        points.values.append(KeyValue('y',str(start[1])))

        points.values.append(KeyValue('z',str(z)))

        points.values.append(KeyValue('type','MOVE'))

        points.values.append(KeyValue('type2','drawCloseStart'))
        da.status.append(points)
        # 添加到容器中
        self.points.append(point)
        end = int(ele.end.real), int(ele.end.imag)
        z = 45.55
        point = {'x': str(end[0]), 'y': str(end[1]), 'z': str(z), 'type': 'UP',  'type2': 'drawCloseEnd'}
        points=DiagnosticStatus()
        points.values.append(KeyValue('x',str(end[0])))

        points.values.append(KeyValue('y',str(end[1])))

        points.values.append(KeyValue('z',str(z)))

        points.values.append(KeyValue('type','UP'))

        points.values.append(KeyValue('type2','drawCloseEnd'))
        da.status.append(points)
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
            #print(translates.find("("))
            #print(scales.find("("))
            # 位移
            self.translate = translates[translates.find("(") + 1:len(translates) - 1].split(',')
            # 缩放比例
            self.scales = scales[scales.find("(") + 1:len(scales) - 1].split(',')

        #print(self.w, self.h)
        pathsList = []
        for path in paths:
            pathsList.append(path.getAttribute('d'))
        # 解析路径字符串
        for path in pathsList:
            result = parse_path(path)
            # path  序列  可以通过for循环获取所有的元素
            for ele in result:
                #print(type(ele).__name__)
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
            #print("area1: ".format(area))
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
        #print(self.result)
        filepath1="img/{}.svg".format(self.result)
        # 1.读取xml文件
        doc = minidom.parse(filepath1)
        # 2.查找path标签
        paths = doc.getElementsByTagName('path')
        svgTag = doc.getElementsByTagName('svg')
        self.w = svgTag[0].getAttribute('width')
        self.h = svgTag[0].getAttribute('height')
        #print(self.w, self.h)
        pathsList = []
        for path in paths:
            pathsList.append(path.getAttribute('d'))
        # 解析路径字符串
        for path in pathsList:
            result = parse_path(path)
            # path  序列  可以通过for循环获取所有的元素
            for ele in result:
                #print(type(ele).__name__)
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

    # 通过摄像头识别写字
    def paintEvent_byVideo(self, result,da):
        filepath1 = "./src/demour/scripts1/img/{}.svg".format(result)
        # 1.读取xml文件
        doc = minidom.parse(filepath1)
        # 2.查找path标签
        paths = doc.getElementsByTagName('path')
        svgTag = doc.getElementsByTagName('svg')
        self.w = svgTag[0].getAttribute('width')
        self.h = svgTag[0].getAttribute('height')
        #print(self.w, self.h)
        pathsList = []
        for path in paths:
            pathsList.append(path.getAttribute('d'))
        # 解析路径字符串
        for path in pathsList:
            result = parse_path(path)
            # path  序列  可以通过for循环获取所有的元素
            for ele in result:
                #print(type(ele).__name__)
                if type(ele).__name__ == 'Move':
                    self.drawMove(ele,da)
                elif type(ele).__name__ == 'Line':
                    self.drawLine(ele,da)
                elif type(ele).__name__ == 'CubicBezier':
                    self.drawCubicBezier(ele,da)
                elif type(ele).__name__ == 'QuadraticBezier':
                    self.drawQuadraticBezier(ele,da)
                elif type(ele).__name__ == 'Close':
                    self.drawClose(ele,da)
                else:
                    print('其他')

# from std_msgs.msg import String
#from geometry_msgs.msg import Twist
## rosrun usb_cam usb_cam_node
## rosrun demour getImage.py
# python订阅者回调在子线程中
# cat ~/.bashrc
# vim ~/.bashrc
# source ~/.bashrc
#如果没有加-v7.3(save('data.mat','test','-v7.3')),

# WARNING:root:Limited tf.compat.v2.summary API due to missing TensorBoard installation.



cvBridge=CvBridge()
## ros file
file="./src/demour/scripts1/h5/abc.h5"
## ide 启动
# file="/h5/abc.h5"
def callBack(msg):
    if not isinstance(msg, Image):
        return
    mat = cvBridge.imgmsg_to_cv2(msg, "bgr8")
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (10, 10));
    # 膨胀
    dst = cv.erode(mat, kernel)
    hsv = cv.cvtColor(dst, cv.COLOR_BGR2HSV)
    lowerb = (0, 0, 113)
    upperb = (225, 255, 255)
    mask = cv.inRange(hsv, lowerb, upperb)
    mask = mask[143:405, 177:596]
    blurred = cv.GaussianBlur(mask, (5, 5), 0)
    edged = cv.Canny(blurred, 30, 150)
    cv.imshow("mask", mask)
    #cv.imshow("edged", edged)
    _, contours, _ = cv.findContours(edged.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    #print("len(contours):{}".format(len(contours)))
    cv.waitKey(100)
    ## 基于外边框的坐标， 提取包裹数字的矩形
    if len(contours)==1:
        area = cv.contourArea(contours[0])
        #print("area:{} ".format(area))
        (x, y, w, h) = cv.boundingRect(contours[0])
        # 把大小改成28*28
        mask = mask[y - 10:y + h + 10, x - 10:x + w + 10]
        cv.imshow("maskaa", mask)
        cv.waitKey(10)
        if area>1800:
            print("=========-----------------------================")
            aa = cv.resize(mask, (28, 28))
            # 把白底黑字 换成 黑底白字
            pre_image = 255 - aa
            cv.imshow("img", pre_image)
            ACTION_ESC = 27;
            ACTION_SPACE = 32;
            cv.waitKey(50)
            print("===============1==========")
            model = tf.keras.models.load_model(file)
            predict = model.predict(pre_image.reshape(1, 28, 28, 1))
            print(predict)
            ## 看哪个出现的次数最多。
            result = np.argmax(predict)
            print("识别的数字:{}".format(result))
            print(type(result))
            da=DiagnosticArray()
            svg.paintEvent_byVideo(str(result),da)
            #print("len(svg.points):{} ".format(len(svg.points)))
            print("len(da.status):{} ".format(len(da.status)))
            publisher.publish(da)

            print("------------2--------------")


# def callBack1(msg):
#     if not isinstance(msg, Image):
#         return
#     mat = cvBridge.imgmsg_to_cv2(msg, "bgr8")
#     print(mat.shape)
#     mat=cv.cvtColor(mat,cv.COLOR_BGR2GRAY)
#     cv.imshow("mat", mat)
#     cv.waitKey(10)
#     model = tf.keras.models.load_model(file)
#     #mat=cv.resize(mat,(28,28))
#     mat1=mat.reshape(1, 28, 28, 1)
#     cv.imshow("mat1", mat1)
#     cv.waitKey(10)
#     predict = model.predict(mat1)
#     print(predict)
#     ## 看哪个出现的次数最多。
#     result = np.argmax(predict)
#     print("识别的数字:{}".format(result))
#     print(type(result))
#     da=DiagnosticArray()
#     svg.paintEvent_byVideo(str(result),da)
#     #print("len(svg.points):{} ".format(len(svg.points)))
#     print("len(da.status):{} ".format(len(da.status)))
#     publisher.publish(da)
#     print("------------2--------------")

def callBack2(msg):

    s=String()
    s.data="123"
    publisher.publish(s)
    print("------------2--------------")

if __name__ == '__main__':
    #print '主线程线程id:{}'.format(threading.current_thread().name)
    # 节点名
    nodeName = 'getImage_node'
    # 初始化节点 定义匿名节点加参数 anonymous=True
    #rospy.init_node(nodeName,anonymous=True)
    rospy.init_node(nodeName)
    # topic名字  /usb_cam/image_raw
    topicName = '/usb_cam/image_raw'
    #topicName = 'image_topic'
    svg=svgPain()
    publisher = rospy.Publisher("tensorflow_node_result", DiagnosticArray, queue_size=5)
    # 创建订阅者
    # 参数1：topic名字
    # 参数2：topic数据类型
    # 参数3：回调函数
    subscriber = rospy.Subscriber(topicName, Image, callBack)
    # 事件处理

    rospy.spin()


# def callBack1(msg):
#     if not isinstance(msg, Image):
#         return
#     mat = cvBridge.imgmsg_to_cv2(msg, "bgr8")
#     cv.imshow("mat", mat)
#     cv.waitKey(10)
#     model = tf.keras.models.load_model(file)
#     predict = model.predict(mat)
#     mat1=mat.reshape(1, 28, 28, 1)
#     cv.imshow("mat1", mat1)
#     cv.waitKey(10)
#     predict = model.predict(mat1)
#     print(predict)
#     ## 看哪个出现的次数最多。
#     result = np.argmax(predict)
#     print("识别的数字:{}".format(result))
#     print(type(result))
#     da=DiagnosticArray()
#     svg.paintEvent_byVideo(str(result),da)
#     #print("len(svg.points):{} ".format(len(svg.points)))
#     print("len(da.status):{} ".format(len(da.status)))
#     publisher.publish(da)
#     print("------------2--------------")


