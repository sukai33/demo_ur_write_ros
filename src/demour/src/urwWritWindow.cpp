//
// Created by sk on 2020/8/31.
//

#include "urwWritWindow.h"

urwWritWindow::urwWritWindow() {

    //初始化界面
    initUI();
    //设置回调
    setCallBack();
    //按钮点击事件
    bindSignal();
}

void urwWritWindow::initUI() {
    setFixedSize(600, 800);
    //布局
    QFormLayout *layout = new QFormLayout;
    QHBoxLayout  *Hlayout = new QHBoxLayout;
    QVBoxLayout  *Vlayout = new QVBoxLayout;
    QLabel *qLabel=new QLabel;
    //ip输入框
    ipEdit = new QLineEdit("192.168.36.26");
    //端口输入框
    portEdit = new QLineEdit("30003");

    //连接状态
    statusLabelEdit = new QLineEdit("未连接");

    //连接机械臂按钮
    connectBtn = new QPushButton("连接机械臂");
    disConnectBtn = new QPushButton("断开连接");
    // 创建两个按钮
    clearBtn = new QPushButton("清理");
    paintBtn = new QPushButton("绘制");

    //自定义控件
    paintWidget = new PaintWidget();

    //连接ip
    QHBoxLayout  *Hlayout_ip = new QHBoxLayout;
    QLabel *qLabel_ip=new QLabel;
    //连接prot
    QHBoxLayout  *Hlayout_port = new QHBoxLayout;
    QLabel *qLabel_port=new QLabel;
    //连接状态
    QHBoxLayout  *Hlayout_statusLabel = new QHBoxLayout;
    QLabel *qLabel_statusLabel=new QLabel;

    //movej的每一个关节输入
    joint1Edit = new QLineEdit("-144.98");
    joint2Edit = new QLineEdit("-97.67");
    joint3Edit = new QLineEdit("-102.98");
    joint4Edit = new QLineEdit("-68.95");
    joint5Edit = new QLineEdit("83.07");
    joint6Edit = new QLineEdit("58.15");

    //movej
    movejBtn = new QPushButton("moveJ");

    //movel输入
    xEdit = new QLineEdit("-54.16");
    yEdit = new QLineEdit("-324.52");
    zEdit = new QLineEdit("183.76");
    rxEdit = new QLineEdit("3.1225");
    ryEdit = new QLineEdit("0.5556");
    rzEdit = new QLineEdit("0.2693");

    //movel
    movelBtn = new QPushButton("moveL");

    //连接ip
    qLabel_ip->setText("ip");
    Hlayout_ip->addWidget(qLabel_ip);
    Hlayout_ip->addWidget(ipEdit);
    //连接prot
    qLabel_port->setText("prot");
    Hlayout_port->addWidget(qLabel_port);
    Hlayout_port->addWidget(portEdit);
    //连接状态
    qLabel_statusLabel->setText("连接状态");
    Hlayout_statusLabel->addWidget(qLabel_statusLabel);
    Hlayout_statusLabel->addWidget(statusLabelEdit);
    Vlayout->addLayout(Hlayout_ip);
    Vlayout->addLayout(Hlayout_port);
    Vlayout->addLayout(Hlayout_statusLabel);

    //链接
    Vlayout->addWidget(connectBtn);
    //断开
    Vlayout->addWidget(disConnectBtn);

    //清理和绘制的按钮
    Hlayout->addWidget(clearBtn);
    Hlayout->addWidget(paintBtn);
    Vlayout->addLayout( Hlayout);
    //添加到整体布局中
    Vlayout->addWidget(paintWidget);


   /* layout->addRow("关节1:", joint1Edit);
    layout->addRow("关节2:", joint2Edit);
    layout->addRow("关节3:", joint3Edit);
    layout->addRow("关节4:", joint4Edit);
    layout->addRow("关节5:", joint5Edit);
    layout->addRow("关节6:", joint6Edit);

    layout->addRow("", movejBtn);

    layout->addRow("x:", xEdit);
    layout->addRow("y:", yEdit);
    layout->addRow("z:", zEdit);
    layout->addRow("rx:", rxEdit);
    layout->addRow("ry:", ryEdit);
    layout->addRow("rz:", rzEdit);

    layout->addRow("", movelBtn);*/

    //设置布局
    //setLayout(layout);
    setLayout(Vlayout);



}



void urwWritWindow::bindSignal() {
    //连接机械臂
    connect(connectBtn,&QPushButton::clicked,this,&urwWritWindow::connectToRobot);
    //断开连接
    connect(disConnectBtn,&QPushButton::clicked,this,&urwWritWindow::disConnectToRobot);
//    //movej信号
//    connect(movejBtn,&QPushButton::clicked,this,&urwWritWindow::movej);
//    //movel信号
//    connect(movelBtn,&QPushButton::clicked,this,&urwWritWindow::movel);

    // 设置按钮点击事件
    // 槽函数可以是普通函数 也可以是类的方法
    connect(clearBtn,&QPushButton::clicked,this,&urwWritWindow::clear);
    // 绘制事件
    connect(paintBtn,&QPushButton::clicked,this,&urwWritWindow::paint);

}

void urwWritWindow::connectToRobot() {
    //通过机器人驱动库  连接机器人
    //ip
    URDriver::getInstance()->connectToRobot(ipEdit->text(),portEdit->text().toInt());
}

void urwWritWindow::disConnectToRobot() {
    URDriver::getInstance()->disConnectToRobot();
}

void urwWritWindow::setCallBack() {
    //连接回调
    URDriver::getInstance()->setConnectCallBack([this]{
        //更新界面状态
       // statusLabel->setText("已连接");
        statusLabelEdit->setText("已连接");
    });

    //断开连接回调
    URDriver::getInstance()->setDisConnectCallBack([this]{
        //更新界面状态
       // statusLabel->setText("未连接");
        statusLabelEdit->setText("未连接");
    });
}

void urwWritWindow::movej() {
    //获取6个关节角度
    double joint1 = joint1Edit->text().toDouble()*DEGREETORADIUS;
    double joint2 = joint2Edit->text().toDouble()*DEGREETORADIUS;
    double joint3 = joint3Edit->text().toDouble()*DEGREETORADIUS;
    double joint4 = joint4Edit->text().toDouble()*DEGREETORADIUS;
    double joint5 = joint5Edit->text().toDouble()*DEGREETORADIUS;
    double joint6 = joint6Edit->text().toDouble()*DEGREETORADIUS;
    //关节角度
    double joints[]{joint1,joint2,joint3,joint4,joint5,joint6};
    //移动机械臂
    URDriver::getInstance()->movej(joints);

//    movel();
}

void urwWritWindow::movel() {
    //获取位置和姿态
    double x = xEdit->text().toDouble()/1000;
    double y = yEdit->text().toDouble()/1000;
    double z = zEdit->text().toDouble()/1000;
    double rx = rxEdit->text().toDouble();
    double ry = ryEdit->text().toDouble();
    double rz = rzEdit->text().toDouble();
    //位置和姿态
    double pose[]{x,y,z,rx,ry,rz};
    //调用驱动的movel方法
    URDriver::getInstance()->movel(pose);
}

//清理画板
void urwWritWindow::clear(){
    paintWidget->clear();
}
//绘制
void urwWritWindow::paint(){
    vector<map<string ,double>> points= paintWidget->getPoints();

    if(points.empty()){
        return;
    }
    
    // 遍历所有的点,移动过去
    for (int i = 0; i <points.size() ; ++i) {
      //  cout<<" points.size()"<<points.size()<<endl;
//        double px = points[i]["x"];
//        double py = points[i]["y"];
//        double pz = points[i]["z"];
//        double xy[2];
//        this->scaleData(px,py,xy);
//        cout<<" 0type==2:x"<<xy[0]/M<<endl;
//        cout<<" 0type==2:y"<<xy[1]/M<<endl;
//        cout<<" 0type==2: pz/M:"<<pz/M<<endl;
//        //位置和姿态
//
//        double pose[]{xy[0]/M,xy[1]/M,pz/M, 3.1401, -0.0002, 0.0000};
//        //调用驱动的movel方法
//        URDriver::getInstance()->movel(pose);




       if(points[i]["type"]==0){

           double px = points[i]["x"];
           double py = points[i]["y"];
            double pz = points[i]["z"];
            double xy[2];
            this->scaleData(px,py,xy);
            cout<<" 0type==0:x"<<xy[0]/M;
            cout<<" 0type==0:y"<<xy[1]/M;
            cout<<" 0type==0: pz/M:"<<pz/M<<endl;
            //位置和姿态
            //double pose1[]{xy[0]/M,xy[1]/M,(double)45.0/M, 3.1401, -0.0002, 0.0000};
            //调用驱动的movel方法
            //URDriver::getInstance()->movel(pose1);
            // URDriver::getInstance()->movep(pose1);
            double pose[]{xy[0]/M,xy[1]/M,(double)pz/M, 3.1401, -0.0002, 0.0000};
            //调用驱动的movel方法
           URDriver::getInstance()->movel(pose);
           //URDriver::getInstance()->movep(pose);
        }else if(points[i]["type"]==2){
           double px = points[i-1]["x"];
           double py = points[i-1]["y"];
            double pz = points[i-1]["z"];
            double xy1[2];
            this->scaleData(px,py,xy1);
            cout<<" 2-1type==2-1:x "<<xy1[0]/M;
            cout<<" 2-1type==2-1:y "<<xy1[1]/M;
            cout<<" 2-1ype==2-1:pz/M:"<<pz/M<<endl;
            //位置和姿态
            double pose[]{xy1[0]/M,xy1[1]/M,pz/M, 3.1401, -0.0002, 0.0000};
            //调用驱动的movel方法
            URDriver::getInstance()->movel(pose);
           //URDriver::getInstance()->movep(pose);
           double px2 = points[i]["x"];
           double py2 = points[i]["y"];
           double pz2 = points[i]["z"];
            double xy2[2];
            this->scaleData(px2,py2,xy2);
           //movep(p[-0.054312,-0.426565,0.03025,3.1401,-0.0002,0.0], a=1.2, v=0.25, r=0)
            //位置和姿态
            double pose2[]{xy2[0]/M,xy2[1]/M,(double)pz2/M, 3.1401, -0.0002, 0.0000};
            //调用驱动的movel方法
            URDriver::getInstance()->movel(pose2);
            //URDriver::getInstance()->movep(pose2);
            cout<<" 2type==2: x:"<<xy2[0]/M;
            cout<<" 2type==2: y:"<<xy2[1]/M;
            cout<<" 2type==2: pz/M:"<<pz2/M<<endl;


        }



    }

}
void urwWritWindow::scaleData(int x,int y,double xy[2]){

    double x1 = (-241+41)*(double )x/579+41;
    double y1 = (-257+456 ) * (double)y / 585-456;
    //y = (-257 + 456) * y / 480 - 456
    xy[0]=x1;
    xy[1]=y1;

}
urwWritWindow::~urwWritWindow() {

}
