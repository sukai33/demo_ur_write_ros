#!/usr/bin/env python
# coding:utf-8
from enum import Enum

# 点的类型 按下 移动 松开
class TYPE(Enum):
    DOWN = 0
    MOVE = 1
    UP = 2