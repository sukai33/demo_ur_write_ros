//
// Created by sk on 2020/8/31.
//

#ifndef URDRIVERCPP_URWWRITWINDOW_H
#define URDRIVERCPP_URWWRITWINDOW_H
#include <QWidget>
#include <QLineEdit>
#include <QPushButton>
#include <QLabel>
#include <QFormLayout>
#include <iostream>
#include <QString>
#include <QWidget>
#include <QDebug>
#include "driver/URDriver.h"
//#include "URDriver.h"
#include <math.h>
#include "PaintWidget.h"
#include <QHBoxLayout>
class urwWritWindow: public QWidget {
private:
    //角度转弧度
    double DEGREETORADIUS = M_PI/180;
    double M=1000;
    //ip输入框
    QLineEdit *ipEdit;
    //端口输入框
    QLineEdit *portEdit;

    //连接状态
    //QLabel *statusLabel;
    QLineEdit *statusLabelEdit;
    //连接机械臂按钮
    QPushButton *connectBtn;
    QPushButton *disConnectBtn;

    //创建两个按钮 清理 绘制
    QPushButton *clearBtn;
    QPushButton *paintBtn;

    // 创建自定义控件
    PaintWidget *paintWidget;



    //movej的每一个关节输入
    QLineEdit *joint1Edit;
    QLineEdit *joint2Edit;
    QLineEdit *joint3Edit;
    QLineEdit *joint4Edit;
    QLineEdit *joint5Edit;
    QLineEdit *joint6Edit;

    //movej
    QPushButton *movejBtn;

    //movel输入
    QLineEdit *xEdit;
    QLineEdit *yEdit;
    QLineEdit *zEdit;
    QLineEdit *rxEdit;
    QLineEdit *ryEdit;
    QLineEdit *rzEdit;

    //movel
    QPushButton *movelBtn;

public:
    urwWritWindow();

    ~urwWritWindow();
    //初始化ui界面
    void initUI();
    //设置回调
    void setCallBack();
    //按钮点击事件
    void bindSignal();
    //连接
    void connectToRobot();
    //断开连接
    void disConnectToRobot();
    //movej
    void movej();
    //movel
    void movel();
    //清理画板
    void clear();
    //绘制
    void paint();
    void scaleData(int x,int y,double xy[2]);
};


#endif //URDRIVERCPP_URWWRITWINDOW_H
