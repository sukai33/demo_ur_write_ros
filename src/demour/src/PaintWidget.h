//
// Created by sk on 2020/8/31.
//

#ifndef URDRIVERCPP_PAINTWIDGET_H
#define URDRIVERCPP_PAINTWIDGET_H
#include <map>
#include <QWidget>
#include <vector>
#include <QMouseEvent>
#include <QPaintEvent>
#include <QPainter>
#include <QPen>
#include <iostream>

using namespace std;
class PaintWidget: public QWidget {
private:
   // map<string, double> points;
    vector<map<string ,double>> points;
    // 创建画家
    //QPainter painter;
    //创建画笔
    //QPen pen;
public:
    PaintWidget();

    ~PaintWidget();
    //清理画板
    void clear();

    //鼠标按下
    void mousePressEvent(QMouseEvent *event);
    //鼠标移动
    void mouseMoveEvent(QMouseEvent *event);
    // 标松开
    void mouseReleaseEvent(QMouseEvent *event);
    // 制事件
    void paintEvent(QPaintEvent *event);
    vector<map<string ,double>> getPoints();
};


#endif //URDRIVERCPP_PAINTWIDGET_H
