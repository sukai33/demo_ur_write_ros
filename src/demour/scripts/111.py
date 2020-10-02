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
doc = minidom.parse('svg/output.svg')
#doc = minidom.parse('svg/1.svg')
# 2.查找path标签
paths = doc.getElementsByTagName('path')
svgTag = doc.getElementsByTagName('svg')
w = svgTag[0].getAttribute('width')
h = svgTag[0].getAttribute('height')
print(type(w),h)

##获取位移与缩放比例
gs = doc.getElementsByTagName('g')
translates_scales=gs[0].getAttribute('transform').split(" ")
if len(translates_scales)>1:
    translates,scales=translates_scales
    print(translates.find("("))
    print(scales.find("("))
    #位移
    translate=translates[translates.find("(")+1:len(translates)-1].split(',')
    #缩放比例
    scales=scales[scales.find("(")+1:len(scales)-1].split(',')
    print(translate)
    print(scales)
