#!/usr/bin/env python
# coding:utf-8

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter,QPen,QColor
from locals import *
'''
绘制自定义控件
paintEvent只会在界面第一次显示的时候主动调用,后面不再主动调用
'''


class PaintWidget(QWidget):
    def __init__(self):
        super(PaintWidget, self).__init__()
        # 容器,保存鼠标经过的所有的点
        # 点数据类型:字典  {'x':x,'y':y,'type:type}
        self.points = []
        #判断是否是画板手画的
        self.flg=True

    def clear(self):
        '''
        清理画板
        :return:
        '''
        # 清空点的列表
        self.points.clear()
        # 重新绘制
        self.update()


    def mousePressEvent(self, event):
        '''
        鼠标按下
        :param event:
        :return:
        '''
        self.flg = True
        x = event.x()
        y = event.y()
        z = 30.25
        # 创建点

        point = {'x':x,'y':y,'z': z,'type':TYPE.DOWN,'pos':len(self.points),'type2': ''}
        # 添加到容器中
        self.points.append(point)
        # 主动绘制
        # update 自动调用paintEvent
        self.update()

    def mouseMoveEvent(self, event):
        '''
        鼠标移动
        :param event:
        :return:
        '''
        self.flg = True
        x = event.x()
        y = event.y()
        z = 30.25
        # 创建点
        point = {'x': x, 'y': y,'z': z, 'type': TYPE.MOVE,'pos':len(self.points),'type2': ''}
        # 添加到容器中
        self.points.append(point)
        # 主动绘制
        self.update()

    def mouseReleaseEvent(self, event):
        '''
        鼠标松开
        :param event:
        :return:
        '''
        self.flg = True
        x = event.x()
        y = event.y()
        z=45.55
        # 创建点
        #point = {'x': x, 'y': y, 'type': TYPE.UP}
        point = {'x': x, 'y': y,'z': z, 'type': TYPE.UP,'pos':len(self.points),'type2': ''}
        # 添加到容器中
        self.points.append(point)
        # 主动绘制
        self.update()

    def paintEvent(self, event):
        '''
        绘制事件
        :param event:
        :return:
        '''
        # 如果点的列表为空,不需要绘制
        if len(self.points)==0:
            return

        # 创建画家
        painter = QPainter(self)
        # 创建画笔
        pen = QPen()
        # 设置画笔颜色
        pen.setColor(QColor(255,0,0))
        # 设置画笔
        painter.setPen(pen)

        if self.flg:
            # 绘制已经走过的点  10个点,如何绘制
            startPoint = self.points[0]
            for index in range(1,len(self.points)):
                # 获取结束的点
                endPoint = self.points[index]
                # 绘制
                if not startPoint['type']==TYPE.UP:
                    painter.drawLine(startPoint['x'], startPoint['y'], endPoint['x'], endPoint['y'])
                # 修改起点
                startPoint = endPoint
        else:
            # 绘制已经走过的点  10个点,如何绘制
            drawLineStart = {}
            drawQuadraticBezierStart = {}
            drawCubicBezierStart = {}
            drawCloseStart = {}
            for index in range(1,len(self.points)):

                if self.points[index]['type2'] == 'drawLineStart':
                    drawLineStart = self.points[index]
                    pass
                if self.points[index]['type2'] == 'drawQuadraticBezierStart':
                    drawQuadraticBezierStart = self.points[index]
                    pass
                if self.points[index]['type2'] == 'drawCubicBezierStart':
                    drawCubicBezierStart = self.points[index]
                    pass
                if self.points[index]['type2'] == 'drawCloseStart':
                    drawCloseStart = self.points[index]
                    pass

                if self.points[index]['type2'] == 'drawMoveStart':
                    painter.drawLine(self.points[index]['x'], self.points[index]['y'], self.points[index]['x'], self.points[index]['y'])
                    pass

                if  self.points[index]['type2']=='drawLineEnd':
                    painter.drawLine(drawLineStart['x'], drawLineStart['y'], self.points[index]['x'], self.points[index]['y'])
                    drawLineStart = self.points[index]
                    pass


                if  self.points[index]['type2']=='drawQuadraticBezierEnd':
                    painter.drawLine(drawQuadraticBezierStart['x'], drawQuadraticBezierStart['y'], self.points[index]['x'], self.points[index]['y'])
                    drawQuadraticBezierStart = self.points[index]
                    pass

                if  self.points[index]['type2']=='drawCubicBezierEnd':
                    painter.drawLine(drawCubicBezierStart['x'], drawCubicBezierStart['y'], self.points[index]['x'], self.points[index]['y'])
                    drawCubicBezierStart = self.points[index]
                    pass
                if  self.points[index]['type2']=='drawCloseEnd':
                    painter.drawLine(drawCloseStart['x'], drawCloseStart['y'], self.points[index]['x'], self.points[index]['y'])
                    drawCloseStart = self.points[index]
                    pass


            pass


