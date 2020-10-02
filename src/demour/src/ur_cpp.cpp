//
// Created by sk on 2020/9/8.
//
#include <QApplication>
#include <iostream>
#include <std_msgs/String.h>
#include <ros/ros.h>
#include <sstream>
#include <diagnostic_msgs/DiagnosticStatus.h>
#include <diagnostic_msgs/DiagnosticArray.h>
#include <diagnostic_msgs/KeyValue.h>
#include "driver/URDriver.h"
#include <string>
//#include <QApplication>
//#include "urwWritWindow.h"
// rosrun demour ur_cpp_node
using namespace std;
//角度转弧度
double DEGREETORADIUS = M_PI/180;
double M=1000;


void scaleData(int x,int y,double xy[2]){
    double x1 = (-241-41)*(double )x/800;
    double y1 = (-257+456 ) * (double)y / 800-456;
   xy[0]=x1;
   xy[1]=y1;


//    double x1 = (-241+41)*(double )x/579+41;
//    double y1 = (-257+456 ) * (double)y / 585-456;
//    //y = (-257 + 456) * y / 480 - 456
//    xy[0]=x1;
//    xy[1]=y1;

}




void paint1(diagnostic_msgs::DiagnosticArray::ConstPtr data){
    if(data->status.empty()){
        return;
    }
    for (int i = 0; i < data->status.size(); ++i) {
        double px =atof( data->status[i].values[0].value.c_str());
        double py = atof( data->status[i].values[1].value.c_str());
        double pz = atof( data->status[i].values[2].value.c_str());
        double xy[2];
        string type = data->status[i].values[3].value;
        string type2 = data->status[i].values[4].value;
        scaleData(px,py,xy);
        cout<<"  x:"<<xy[0]/M;
        cout<<"  y:"<<xy[1]/M;
        cout<<"  pz:"<<pz/M<<endl;
        cout<<"  type:"<<type<<endl;
        if (type == "DOWN"){
            double pose[]{xy[0]/M,xy[1]/M,45.55/M, 3.1401, -0.0002, 0.0000};
            //调用驱动的movel方法
            URDriver::getInstance()->movel(pose);

            double pose1[]{xy[0]/M,xy[1]/M,(double)pz/M, 3.1401, -0.0002, 0.0000};
            //调用驱动的movel方法
           URDriver::getInstance()->movep(pose1);
        }


        if (type == "MOVE"){
            double pose1[]{xy[0]/M,xy[1]/M,(double)pz/M, 3.1401, -0.0002, 0.0000};
            //调用驱动的movel方法
            //URDriver::getInstance()->movep(pose1);
        }

        if (type == "UP"){

            double pose[]{xy[0]/M,xy[1]/M,30.55/M, 3.1401, -0.0002, 0.0000};
            //调用驱动的movel方法
          //URDriver::getInstance()->movep(pose);

            double pose1[]{xy[0]/M,xy[1]/M,(double)pz/M, 3.1401, -0.0002, 0.0000};
            //调用驱动的movel方法
          //URDriver::getInstance()->movep(pose1);
        }


    }

}


void callBack(diagnostic_msgs::DiagnosticArray::ConstPtr data){
    if(data== nullptr){
        return;
    }
    if(data->status.empty()){
        return;
    }

    for (int i = 0; i < data->status.size(); ++i) {
        diagnostic_msgs::DiagnosticStatus  status = data->status[i];
        if(status.values.empty()){
            return;
        }
        if(status.values.size()<5){
            cout<<"收到消息status.values.size():"<<status.values.size()<<endl;
            return;
        }
        cout<<"收到消息status.values.size():"<<status.values.size()<<endl;
    }
    //驱动机器人写字
    paint1(data);
    cout<<"收到消息--:"<<endl;
//    cout<<"收到消息:"<<data->data<<endl;
//    stringstream ss;
//    ss<<"./src/demour/src/img/";
//    ss<<data->data;
//    ss<<".svg";


}
int ii=true;
int main(int argc, char *argv[]) {



    //节点名
    //    string nodeName = "cpp_subscriber";
    string nodeName = "cpp_ur_publisher";
    //初始化节点
    //ros::init(argc, argv, nodeName);
    //初始化节点 定义匿名节点加参数 ,ros::init_options::AnonymousName
    ros::init(argc,argv,nodeName,ros::init_options::AnonymousName);
    //ros::init(argc,argv,nodeName);
    //创建节点
    ros::NodeHandle node;
    //topic名字
    string topicName = "tensorflow_node_result";

    //订阅者
    //参数1：topic名字
    //参数2：队列长度
    //参数3：回调函数
    //注意：返回的Subscriber必须要接收,如果不接受 可能收不到消息
    const ros::Subscriber &subscriber = node.subscribe<diagnostic_msgs::DiagnosticArray>(topicName, 5, callBack);
    //ros::spin 处理事件
    // ros::spin();
     ros::AsyncSpinner spinner(1);

    QApplication app(argc,argv);
    if(ii){
        URDriver::getInstance()->connectToRobot("192.168.36.26",30003);
    }
    ii=false;
     return QApplication::exec();
    //return 0;
}


//int main(int argc, char *argv[]) {
//    QApplication app(argc, argv);
//    //机器人写字
//    //auboWritWion w;
//    urwWritWindow w;
//    //测试ur
//    // 创建窗口
//    //MainWindow w;
//    //显示窗口
//    w.show();
//    return QApplication::exec();
//}