#!/usr/bin/env python
# coding:utf-8
# 读取svg的xml文件

from xml.dom import minidom
# 解析svg路径
from svg.path import parse_path
import numpy as np
import cv2 as cv
import random

# 1.读取xml文件
doc = minidom.parse('svg/che.svg')
# 2.查找path标签
paths = doc.getElementsByTagName('path')
svgTag = doc.getElementsByTagName('svg')
w = svgTag[0].getAttribute('width')
h = svgTag[0].getAttribute('height')
print(type(w),h)

# 定义列表 保存所有的path的d属性 pip3  install svg.path
pathsList = []
for path in paths:
    pathsList.append(path.getAttribute('d'))

# ------------------------- 颜色 -------------------------#
RED = (0, 0, 255)


# 随机颜色
def randomColor():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


# ------------------------- 绘制 -------------------------#
dst = np.zeros((1920, 1080, 3), dtype=np.uint8)


# ------------------------- 绘制move -------------------------#
def drawMove(ele):
    start = int(ele.start.real), int(ele.start.imag)
    cv.line(dst, start, start, randomColor())
    cv.imshow('dst', dst)
    cv.waitKey(5)


# ------------------------- 绘制直线 -------------------------#
# Line(start=(424.81453999999997+371.04679000000004j), end=(424.81453999999997+369.04679000000004j))
def drawLine(ele):
    start = int(ele.start.real), int(ele.start.imag)
    end = int(ele.end.real), int(ele.end.imag)
    cv.line(dst, start, end, RED)
    cv.imshow('dst', dst)
    cv.waitKey(5)


# ------------------------- 绘制二阶贝塞尔 -------------------------#
def QuadraticBezier(ps, pc, pe, t):
    '''
    获取二阶贝塞尔点
    :param ps: 开始点
    :param pc: 控制点
    :param pe: 结束点
    :param t: 0-1
    :return:
    '''
    return pow(1 - t, 2) * ps + 2 * t * (1 - t) * pc + pow(t, 2) * pe


def drawQuadraticBezier(ele):
    # 开始点
    ps = np.array([ele.start.real, ele.start.imag])
    # 控制点
    p = np.array([ele.control.real, ele.control.imag])
    # 结束点
    pe = np.array([ele.end.real, ele.end.imag])
    point = QuadraticBezier(ps, p, pe, 0)
    start = int(point[0]), int(point[1])
    # 40个点
    for i in range(1, 41):
        result = QuadraticBezier(ps, p, pe, i / 40)
        end = int(result[0]), int(result[1])
        # 连接两个点
        cv.line(dst, start, end, randomColor())
        cv.imshow('dst',dst)
        cv.waitKey(5)
        # 开始点变成结束点
        start = end


# ------------------------- 三阶贝塞尔 -------------------------#
def CubicBezier(ps, pc1, pc2, pe, t):
    '''
    获取二阶贝塞尔点
    :param ps: 开始点
    :param pc: 控制点
    :param pe: 结束点
    :param t: 0-1
    :return:
    '''
    return pow(1 - t, 3) * ps + 3 * t * pow(1 - t, 2) * pc1 + 3 * pow(t, 2) * (1 - t) * pc2 + pow(t, 3) * pe


def drawCubicBezier(ele):
    print('绘制贝塞尔')
    # 开始点
    ps = np.array([ele.start.real, ele.start.imag])
    # 控制点
    p1 = np.array([ele.control1.real, ele.control1.imag])
    p2 = np.array([ele.control2.real, ele.control2.imag])
    # 结束点
    pe = np.array([ele.end.real, ele.end.imag])
    result = CubicBezier(ps, p1, p2, pe, 0)
    print(result)
    start = int(result[0]),int(result[1])
    # 40个点
    for i in range(1,41):
        result = CubicBezier(ps, p1, p2, pe, i / 40)
        end = int(result[0]),int(result[1])
        # 连接两个点
        cv.line(dst,start,end,randomColor())
        cv.imshow('dst',dst)
        cv.waitKey(5)
        # 开始点变成结束点
        start = end

#------------------------- 结束点 -------------------------#
def drawClose(ele):
    start = int(ele.start.real), int(ele.start.imag)
    end = int(ele.end.real), int(ele.end.imag)
    cv.line(dst, start, end, randomColor())
    cv.imshow('dst', dst)
    cv.waitKey(5)

# 解析路径字符串
for path in pathsList:
    result = parse_path(path)
    print(result)
    # path  序列  可以通过for循环获取所有的元素
    for ele in result:
        print(type(ele).__name__)
        if type(ele).__name__ == 'Move':
            drawMove(ele)
        elif type(ele).__name__ == 'Line':
            drawLine(ele)
        elif type(ele).__name__ == 'CubicBezier':
            drawCubicBezier(ele)
        elif type(ele).__name__ == 'QuadraticBezier':
            drawQuadraticBezier(ele)
        elif type(ele).__name__ == 'Close':
            drawClose(ele)
        else:
            print('其他')

cv.waitKey(0)
