//
// Created by wt on 2020/9/7.
//
#include <iostream>
#include <ros/ros.h>
#include <sensor_msgs/Image.h>
using namespace std;

void callBack(sensor_msgs::Image::ConstPtr image){
    cout<<"图像数据"<<endl;
}

int main(int argc,char *argv[]){
    //节点名
    string nodeName = "first_node";
    //初始化节点
    ros::init(argc,argv,nodeName);
    //创建节点
    ros::NodeHandle node;
    /*-------------------------- 获取摄像头数据 --------------------------*/
    //topic名字
    string topicName = "/usb_cam/image_raw";
    const ros::Subscriber &subscriber = node.subscribe<sensor_msgs::Image>(topicName, 10, callBack);

    //事件轮询
    ros::spin();
    return 0;
}
