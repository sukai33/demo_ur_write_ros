//
// Created by wt on 2020/9/7.
//
#include <iostream>
#include <ros/ros.h>
#include <sensor_msgs/Image.h>
#include <image_transport/image_transport.h>
#include <cv_bridge/cv_bridge.h>
#include <sensor_msgs/image_encodings.h>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
#include "sensor_msgs/Image.h"
using namespace std;
int seq = 0;
void callBack(sensor_msgs::Image::ConstPtr image,const ros::Publisher *publisher){

    //转opencv
    const cv_bridge::CvImageConstPtr &ptr = cv_bridge::toCvShare(image,"bgr8");
    cv::Mat mat = ptr->image;
    //处理
    //opev显示
//    cv::imshow("dst",mat);
//    cv::waitKey(3);
    //传递处理之后的Mat
    cv_bridge::CvImage newImage;
    newImage.header.seq = ++seq;
    newImage.header.stamp = ros::Time::now();
    newImage.image = mat;
    newImage.encoding = "bgr8";
    //转opencv转数据msg传输
    const sensor_msgs::ImagePtr &image_msg = newImage.toImageMsg();
    //发布topic
    publisher->publish(image_msg);
}

int main(int argc,char *argv[]){
    //节点名
    string nodeName = "first_node";
    //初始化节点
    ros::init(argc,argv,nodeName);
    //创建节点
    ros::NodeHandle node;

    /*-------------------------- 发布者 --------------------------*/
    //topic名字
    string publishName = "image_topic";
    const ros::Publisher &publisher = node.advertise<sensor_msgs::Image>(publishName, 10);

    /*-------------------------- 获取摄像头数据 --------------------------*/
    //topic名字
    string topicName = "/usb_cam/image_raw";
    const ros::Subscriber &subscriber = node.subscribe<sensor_msgs::Image>(topicName, 10, bind(callBack,_1,&publisher));

    //事件轮询
    ros::spin();
    return 0;
}
