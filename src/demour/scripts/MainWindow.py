#!/usr/bin/env python
# coding:utf-8
from PyQt5.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QPushButton
from PaintWidget import PaintWidget
#from sdk.ur import UR
import urx
import math
from locals import *
from svg_class import *
import threading
class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.DE2R = math.pi / 180
        self.M=1000
        # # 机器人驱动
        # self.ur = UR()
        self.robot = urx.Robot("192.168.36.26")
        # # 连接
        # self.ur.connect()
        # 设置标题
        self.setWindowTitle('机器人绘制')
        # 设置窗口大小
        self.setFixedSize(640,480)
        # 创建整体布局
        wholeLayout = QVBoxLayout()
        # 设置布局
        self.setLayout(wholeLayout)
        # 创建上部布局
        topLayout = QHBoxLayout()
        # 添加布局到整体布局中
        wholeLayout.addLayout(topLayout)
        # 创建两个按钮
        clearBtn = QPushButton('清理')
        paintBtn = QPushButton('画板写字')
        paintBtn1 = QPushButton('svg图片写字')
        paintBtn2 = QPushButton('识别预存图片写字')
        paintBtn3 = QPushButton('摄像头识别图片写标准字')
        paintBtn4 = QPushButton('摄像头识别图片写原字')

        # 按钮添加到布局中
        topLayout.addWidget(clearBtn)
        topLayout.addWidget(paintBtn)
        topLayout.addWidget(paintBtn1)
        topLayout.addWidget(paintBtn2)
        topLayout.addWidget(paintBtn3)
        topLayout.addWidget(paintBtn4)

        ## 获取手写板数据
        # 创建自定义控件
        self.paintWidget = PaintWidget()
        # 添加到整体布局中
        wholeLayout.addWidget(self.paintWidget)

        ##获取svg数据
        self.svg = svgPain()



        # 设置按钮点击事件
        # 槽函数可以是普通函数 也可以是类的方法
        clearBtn.clicked.connect(self.clear)
        # 通过画板写字 绘制事件
        paintBtn.clicked.connect(self.paint)
        #通过svg图片写字
        paintBtn1.clicked.connect(self.paint_svg)
        # 识别手写字图片写字 识别预存图片写字
        paintBtn2.clicked.connect(self.paint_svg_byImgae)
        # 摄像头识别写标准字
        paintBtn3.clicked.connect(self.paint_svg_byImgae_Video)
        # 摄像头识别写原字
        paintBtn4.clicked.connect(self.paint_svg_byImgae_Video_withSVG)



    def clear(self):
        '''
        清理
        :return:
        '''
        self.paintWidget.clear()

    def scaleData(self,x,y):
        '''
        对数据缩放处理
        :param cal:
        :return:
        '''


        x = (-241-41)*x/800
        y = (-257+456 ) * y / 800-456
        return x,y

    def getChangF(self,y,translate):
        #位移
        translate_index = translate.find(".")
        translate_int = int(translate[:translate_index if (translate_index > 1) else len(translate)])
        if (translate_int > 0):
            y = y - 1.5 * (y -translate_int)
        return y

    def scaleData_with_wh(self,px,py,w,h,translate):
        '''
        对数据缩放处理
        :param cal:
        :return:
        '''
        h_index = h.find(".")
        w_index = w.find(".")
        h = int(h[:h_index if (h_index > 1) else len(h)])
        w = int(w[:w_index if (w_index > 1) else len(w)])
        print("-------------------------")
        print(w)
        print(h)
        print("----------px---------------")
        print(px)
        print("----------py---------------")
        print(py)
        print("----------x_p---------------")
        # 位移
        #translate_index = translate.find(".")
        #translate_int = int(translate[:translate_index if (translate_index > 1) else len(translate)])

        # x = (260 + 60) * x / w
        # y = self.getChangF(y,translate)
        # y = (-220 + 470) * y / h - 470
        x_p,y_p = self.getWH(h, w, y_p=250)
        print(x_p)
        x = -x_p * px / w
        py = self.getChangF(py,translate)
        y = y_p * py / h- 456

        return x,y
    ##获取写字板的宽高,通过实际字体的大小求
    def getWH(self,h,w,y_p=250):
        # 1.取最小的(高度最小) h: y_p高度尺寸, 按原始画布的宽高比例计算出宽度尺寸x_p
        x_p = y_p * w / h
        return x_p,y_p
        pass
    def scaleData_with_wh_svg(self,px,py,w,h):
        '''
        对数据缩放处理
        :param cal:
        :return:
        px :原图像x坐标
        py :原图像y坐标
        w  :原图像所在的画布宽度
        h  :原图像所在的画布宽度

        映射的画布尺寸 w:640 h: 480
        1.取最小的(高度最小) h: y_p高度尺寸,按原始画布的宽高比例计算出宽度尺寸x_p
        2.通过原始图像px坐标与原始画布w宽度的比例计算出映射画布的图像x坐标
        3.通过原始图像py坐标与原始画布h宽度的比例计算出映射画布的图像y坐标

        '''
        h_index=h.find(".")
        w_index = w.find(".")
        h=int(h[:h_index if (h_index>1) else len(h)])
        w=int(w[:w_index if (w_index>1) else len(w)])
        #1.取最小的(高度最小) h: y_p高度尺寸, 按原始画布的宽高比例计算出宽度尺寸x_p
        y_p = 460
        x_p = y_p * w / h
        #2.通过原始图像px坐标与原始画布w宽度的比例计算出映射画布的图像x坐标
        x =  px *x_p / w
        #3.通过原始图像py坐标与原始画布h宽度的比例计算出映射画布的图像y坐标
        y =  py * y_p/ h
        return x,y

    def scaleData_with_wh2(self,x,y,w,h):
        '''
        对数据缩放处理
        :param cal:
        :return:
        '''

        h_index = h.find(".")
        w_index = w.find(".")
        h = int(h[:h_index if (h_index > 1) else len(h)])
        w = int(w[:w_index if (w_index > 1) else len(w)])

        x = (-241 - 41) * x / w
        y = (-257 + 456) * y / h - 456
        return x,y

    def scaleData_with_wh3(self,x,y,w,h):
        '''
        对数据缩放处理
        :param cal:
        :return:
        '''

        h_index = h.find(".")
        w_index = w.find(".")
        h = int(h[:h_index if (h_index > 1) else len(h)])
        w = int(w[:w_index if (w_index > 1) else len(w)])
        x = (-241 - 41) * x / w
        y = (-257 + 456) * y / h - 456
        return x,y

    def paint(self):
        '''
        调用机器人绘制
        :return:
        '''
        #self.ur.move_j([-84.56, -87.06, -89.02, -96.33, 90.87, 89.87])
        # self.robot.movej([-144.98 * self.DE2R, -97.67 * self.DE2R, -102.98 * self.DE2R, -68.95 * self.DE2R, 83.07 * self.DE2R, 58.15 * self.DE2R], 1.5,
        #             1.05)
        #self.robot.movej([-84.56, -87.06, -89.02, -96.33, 90.87, 89.87])
        #self.robot.movel([-54.16 / 1000, -324.52 / 1000, 183.76 / 1000, 3.1225, 0.5556, 0.2693], 1.2, 0.25)
        # 获取所有的点
        # 绘制点的数量
        # 遍历所有的点,移动过去
        for index,point in enumerate(self.paintWidget.points):
            px = point['x']
            py = point['y']
            pz = point['z']
            x, y = self.scaleData(px, py)
            if point['type'] == TYPE.DOWN:
              self.robot.movel([x / self.M, y / self.M, 45.55 / self.M, 3.1401, -0.0002, 0.0000], 1.2, 0.25)
              self.robot.movep([x / self.M, y / self.M, pz / self.M, 3.1401, -0.0002, 0.0000], 1.2, 0.25)

            if point['type'] == TYPE.MOVE:
                if index%10==0:
                    self.robot.movep([x / self.M, y / self.M, pz / self.M, 3.1401, -0.0002, 0.0000], 1.2, 0.25)

            if point['type'] == TYPE.UP:
                self.robot.movep([x / self.M, y / self.M, 30.55 / self.M, 3.1401, -0.0002, 0.0000], 1.2, 0.25)
                self.robot.movep([x / self.M, y / self.M, pz / self.M, 3.1401, -0.0002, 0.0000], 1.2, 0.25)


    def paint_svg(self):
        '''
        调用机器人绘制
        :return:
        '''
        # 绘制点的数量
        # 遍历所有的点,移动过去 通过svg写字

        self.svg.paintEvent()
        self.paintWidget.flg = False
        self.updatePoints(self.svg.translate[1])
        t=threading.Thread(target=self.printWirt_svg,)
        t.setDaemon(True)
        t.start()

    ##映射画板
    def updatePoints(self,translate):
      if not self.paintWidget.flg:
            del self.paintWidget.points
            self.paintWidget.points = self.svg.points


            # 映射画板
            for index, pt in enumerate(self.paintWidget.points):
                px = pt['x']
                py = pt['y']
                x, y = self.scaleData_with_wh_svg(px, py, self.svg.w, self.svg.h)
                self.paintWidget.points[index]['x'] = x
                y = y = self.getChangF(y,translate)
                self.paintWidget.points[index]['y'] = y

            self.paintWidget.update()


     #通过识别图片写字
    def paint_svg_byImgae(self):
        '''
        调用机器人绘制
        :return:
        '''
        # 绘制点的数量
        # 遍历所有的点,移动过去 通过svg写字
        self.paintWidget.points.clear()
        input_im = cv.imread("img/ccc.bmp")

        self.svg.paintEvent_byImage(input_im)
        self.paintWidget.flg = False
        self.updatePoints()
        t = threading.Thread(target=self.printWirt, )
        t.setDaemon(True)
        t.start()

    #通过摄像头识别图片写标准字
    def paint_svg_byImgae_Video(self):
        '''
        调用机器人绘制
        :return:
        '''
        # 绘制点的数量
        # 遍历所有的点,移动过去 通过svg写字
        self.svg.see_tensorflow_Video()
        self.paintWidget.flg = False
        self.updatePoints()
        t = threading.Thread(target=self.printWirt, )
        t.setDaemon(True)
        t.start()


    #通过摄像头识别图片写字
    def paint_svg_byImgae_Video_withSVG(self):
        '''
        调用机器人绘制
        :return:
        '''
        # 绘制点的数量
        # 遍历所有的点,移动过去 通过svg写字
        self.svg.see_tensorflow_Video_getimage()
        self.paintWidget.flg = False
        self.updatePoints()
        t = threading.Thread(target=self.printWirt, )
        t.setDaemon(True)
        t.start()


    ##发送点坐标数据给ur进行绘制
    def printWirt(self):
        for index,point in enumerate(self.svg.points):
            px = point['x']
            py = point['y']
            pz = point['z']
            x, y = self.scaleData_with_wh(px, py,self.svg.w,self.svg.h,self.svg.translate[1])
            print(x)
            print(y)
            if point['type'] == TYPE.DOWN:
              self.robot.movel([x / self.M, y / self.M, 45.55 / self.M, 3.1401, -0.0002, 0.0000], 1.2, 0.25)
              self.robot.movep([x / self.M, y / self.M, pz / self.M, 3.1401, -0.0002, 0.0000], 1.2, 0.25)
              pass

            if point['type'] == TYPE.MOVE:
                    self.robot.movep([x / self.M, y / self.M, pz / self.M, 3.1401, -0.0002, 0.0000], 1.2, 0.25)
                    pass

            if point['type'] == TYPE.UP:
                self.robot.movep([x / self.M, y / self.M, 30.55 / self.M, 3.1401, -0.0002, 0.0000], 1.2, 0.25)
                self.robot.movep([x / self.M, y / self.M, pz / self.M, 3.1401, -0.0002, 0.0000], 1.2, 0.25)
                pass

    ##发送点坐标数据给ur进行绘制
    def printWirt_svg(self):
        for index,point in enumerate(self.paintWidget.points):
            px = point['x']
            py = point['y']
            pz = point['z']
            x, y = self.scaleData(px, py)

            print(x)
            print(y)
            if point['type'] == TYPE.DOWN:
              self.robot.movel([x / self.M, y / self.M, 45.55 / self.M, 3.1401, -0.0002, 0.0000], 1.2, 0.25)
              self.robot.movep([x / self.M, y / self.M, pz / self.M, 3.1401, -0.0002, 0.0000], 1.2, 0.25)
              pass

            if point['type'] == TYPE.MOVE:
                    self.robot.movep([x / self.M, y / self.M, pz / self.M, 3.1401, -0.0002, 0.0000], 1.2, 0.25)
                    pass

            if point['type'] == TYPE.UP:
                self.robot.movep([x / self.M, y / self.M, 30.55 / self.M, 3.1401, -0.0002, 0.0000], 1.2, 0.25)
                self.robot.movep([x / self.M, y / self.M, pz / self.M, 3.1401, -0.0002, 0.0000], 1.2, 0.25)
                pass



