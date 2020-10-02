//
// Created by wt on 2020/8/28.
//

#ifndef URDRIVERCPP_URDRIVER_H
#define URDRIVERCPP_URDRIVER_H

#include <iostream>
#include <memory>
#include <QTcpSocket>
#include <functional>
#include "URScript.h"
#include <QDebug>
#include "data.h"
#include <memory.h>
#include "utils.h"
#include <queue>
using namespace std;
class URDriver {
private:
    //私有三个构造函数
    URDriver();
    URDriver(const  URDriver&);
    URDriver operator=(const  URDriver&);
    //定义静态变量
    static shared_ptr<URDriver> instance;
    //QTcpSocket
    QTcpSocket socket;
    //创建脚本对象
    URScript script;
    //连接回调函数
    function<void()> connectCallBack;
    //断开连接回调
    function<void()> disConnectCallBack;
    //指令队列
    queue<Instruction> instructionQueue;
    //是否是第一次
    bool isFirst = true;
    //目标位置
    Instruction targetInstruction;
public:
    //静态方法返回当前实例
    static shared_ptr<URDriver> getInstance();
    ~URDriver();
    //连接机器人
    void connectToRobot(QString ip,int port);
    //断开连接
    void disConnectToRobot();
    //设置回调函数
    void setConnectCallBack(function<void()> connectCallBack);
    //设置断开连接回调
    void setDisConnectCallBack(function<void()> disConnectCallBack);
    //movej移动
    void movej(double joints[6],double a=1.4, double v=1.05);
    //movel移动
    void movel(double pose[6],double a=1.2, double v=0.25);
    //movep移动
    void movep(double pose[6],double a=0.5, double v=0.1);
    //解析机器人返回数据
    void parseData(QByteArray &data,URData &urData);
    //添加指令
    void addInstruction(MOVETYPE movetype,double data[6],double a,double v);
    //是否执行下一条指令
    void decideExcuteNextInstruction(URData &urData);
    //执行下一条指令
    void excuteNextInstruction();
    //更新目标指令
    void updateTargetInstruction(Instruction &instruction);
};


#endif //URDRIVERCPP_URDRIVER_H
