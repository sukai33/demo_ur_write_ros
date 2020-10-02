#!/usr/bin/env python
# coding:utf-8
#pip2 install opencv-python==3.4.2.16 -i https://mirror.baidu.com/pypi/simple
#pip2 install svg.path -i https://mirror.baidu.com/pypi/simple
#pip2 install tensorflow -i https://mirror.baidu.com/pypi/simple
#pip2 install math3d -i https://mirror.baidu.com/pypi/simple
import cv2
import rospy
import tensorflow as tf
import os
# model = tf.keras.models.load_model('h5/abc.h5')
# #predict = model.predict(pre_image.reshape(1, 28, 28, 1))
# #print(predict)
# print("123")
import cv2 as cv
path ="{}".format(os.popen("pwd").readline().rstrip('\r\n'))

print (path.rfind("/"))
print (path[0:path.rfind("/")])
print (path)

mat=cv.imread("img/aaa.bmp")
cv.imshow("mat",mat)
cv.waitKey(0)