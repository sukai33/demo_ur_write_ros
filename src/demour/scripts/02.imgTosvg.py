#!/usr/bin/env python
# coding:utf-8
import os


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

def t1(img_path):
    """
    img转svg方法
    :param img_path: img路径
    :return: 返回output.svg绝对路径
    """
    os.system("convert " + img_path + " output_tmp.ppm")
    os.system("potrace output_tmp.ppm -b svg -u 1 --flat -o img/output.svg")
    os.system("rm output_tmp.ppm")
    print("{}/img/output.svg".format(os.popen("pwd").readline().rstrip('\r\n')))


    return "{}/img/output.svg".format(os.popen("pwd").readline().rstrip('\r\n'))

t1('img/chef.jpg')