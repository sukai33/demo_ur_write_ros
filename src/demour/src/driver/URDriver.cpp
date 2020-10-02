//
// Created by wt on 2020/8/28.
//

#include "URDriver.h"

shared_ptr<URDriver> URDriver::instance = shared_ptr<URDriver>(new URDriver);

URDriver::URDriver() {
    //监听connected信号
    QObject::connect(&socket, &QTcpSocket::connected, [this] {
       // connectCallBack();
    });

    //断开连接信号
    QObject::connect(&socket, &QTcpSocket::disconnected, [this] {
       // disConnectCallBack();
    });

    QObject::connect(&socket, &QTcpSocket::readyRead, [this] {
        //读取数据
        QByteArray data = socket.readAll();
        URData urData;
        //解析数据
        parseData(data, urData);
        //决定是否执行下一条指令
        //printf("=================zhixing=============");
        decideExcuteNextInstruction(urData);
        //cout << "=================zhixing=============" << endl;
    });
}

URDriver::~URDriver() {
    cout << "析构函数" << endl;
}

shared_ptr<URDriver> URDriver::getInstance() {
    return instance;
}

void URDriver::connectToRobot(QString ip, int port) {
    socket.connectToHost(ip, port);
}

void URDriver::setConnectCallBack(function<void()> connectCallBack) {
   // this->connectCallBack = connectCallBack;
}

void URDriver::setDisConnectCallBack(function<void()> disConnectCallBack) {
   // this->disConnectCallBack = disConnectCallBack;
}

void URDriver::disConnectToRobot() {
  //  socket.disconnectFromHost();
}

void URDriver::movej(double joints[6], double a, double v) {
    //添加到队列中
    addInstruction(MOVEJ, joints, a, v);
//    //判断状态
//    if(!idle){
//        return;
//    }
//    //发送指令给机械臂  'movej([90,80], a=1.4, v=1.05, t=0, r=0)'
//    //1.拼接发送的指令字符串
//    QString msg = script.loadMovejScript(joints, a, v);
//    //2.通过socket发送拼接的字符串
//    socket.write(msg.toUtf8());
}

void URDriver::movel(double *pose, double a, double v) {
    //添加到队列中
    addInstruction(MOVEL, pose, a, v);
//    //判断状态
//    if(!idle){
//        return;
//    }
//    //1.拼接发送的指令字符串
//    QString msg = script.loadMovelScript(pose, a, v);
//    //2.通过socket发送拼接的字符串
//    socket.write(msg.toUtf8());
}
void URDriver::movep(double *pose, double a, double v) {
    //添加到队列中
    addInstruction(MOVEP, pose, a, v);
//    //判断状态
//    if(!idle){
//        return;
//    }
//    //1.拼接发送的指令字符串
//    QString msg = script.loadMovelScript(pose, a, v);
//    //2.通过socket发送拼接的字符串
//    socket.write(msg.toUtf8());
}
void URDriver::parseData(QByteArray &data, URData &urData) {
    //先解析第一个数据MsgSize
    //拷贝前四个字节  到URData结构体
//    char *pdata = data.data();
    char pdata[1108];
    //把data所有的数据拷贝
    memcpy(pdata, data.data(), data.size());
    /*-------------------------- 定义指针保存首地址 --------------------------*/
    char *p = pdata;
    /*-------------------------- 拷贝前4个字节 --------------------------*/
    //交换前四个字节
    reverseByte(p, 4);
    //拷贝前四个字节
    memcpy(&urData.MsgSize, pdata, 4);
    /*-------------------------- 交换剩下的数据 --------------------------*/
    for (char *q = p + 4; q < p + 1108 - 8; q += 8) {
        //交换这8个数据
        reverseByte(q, 8);
    }
    //拷贝剩下的数据
    memcpy(((char *) &urData) + 8, p + 4, data.size() - 4);
}

void URDriver::addInstruction(MOVETYPE movetype, double *data, double a, double v) {
    //构建指令结构体
    Instruction instruction;
    instruction.movetype = movetype;
    //拷贝data后面6个数据到指令的data中
    memcpy(instruction.data, data, 6 * sizeof(double));
    instruction.a = a;
    instruction.v = v;
    //添加到队列中
    instructionQueue.push(instruction);
}

void URDriver::decideExcuteNextInstruction(URData &urData) {
    if (isFirst) {
        //如果第一次执行  直接执行
        excuteNextInstruction();
    } else {
        //不是第一次执行  判断是否和目标足够接近
        if(isClose(targetInstruction,urData)){
            //执行下一条
            excuteNextInstruction();
        }
    }

}

void URDriver::excuteNextInstruction() {
    //判断是否有指令
    if (instructionQueue.empty()) {
        return;
    }
    //取出一条执行
    Instruction &instruction = instructionQueue.front();
    QString msg;
    if (instruction.movetype == MOVEJ) {
        //执行指令
        msg = script.loadMovejScript(instruction.data, instruction.a, instruction.v);
    } else if (instruction.movetype == MOVEL) {
        msg = script.loadMovelScript(instruction.data,instruction.a,instruction.v);
    }else if (instruction.movetype == MOVEP) {
        //movep(p[-0.0232487,-0.410077,0.045,3.1401,-0.0002,0], a=1.2, v=0.25, r=0)
        msg = script.loadMovepScript(instruction.data,instruction.a,instruction.v);
    }
    cout<<msg.toStdString()<<endl;
    //发送指令
    socket.write(msg.toUtf8());
    //cout<<msg.toStdString()<<endl;
    //修改字段
    isFirst = false;
    //更新目标指令
    updateTargetInstruction(instruction);
    //删除队列中的这条指令
    instructionQueue.pop();
}

void URDriver::updateTargetInstruction(Instruction &instruction) {
    targetInstruction.movetype = instruction.movetype;
    memcpy(targetInstruction.data,instruction.data,6*sizeof(double ));
    targetInstruction.a = instruction.a;
    targetInstruction.v = instruction.v;
}
