#!/usr/bin/env python
# coding:utf-8
class Point:
    PRESS = 0
    MOVE = 1
    RELEASE = 2
    DOWNZ = -0.2
    UPZ = 0.15651
    def __init__(self):
        # # 每一个点类型
        # self.type = []
        # 坐标 x以及y{'type':type,'x'"x,"y":y}
        self.data = []