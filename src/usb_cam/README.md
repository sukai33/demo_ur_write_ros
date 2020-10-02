usb_cam [![Build Status](https://api.travis-ci.org/bosch-ros-pkg/usb_cam.png)](https://travis-ci.org/bosch-ros-pkg/usb_cam)
=======

#### A ROS Driver for V4L USB Cameras
This package is based off of V4L devices specifically instead of just UVC.

For full documentation, see [the ROS wiki](http://ros.org/wiki/usb_cam).

[Doxygen](http://docs.ros.org/indigo/api/usb_cam/html/) files can be found on the ROS wiki.

### License
usb_cam is released with a BSD license. For full terms and conditions, see the [LICENSE](LICENSE) file.

### Authors
See the [AUTHORS](AUTHORS.md) file for a full list of contributors.


## rosrun调试
 
1. 运行`usb_cam`节点
 
   ```bash
   rosrun usb_cam usb_cam_node
   ```
 
2. 图像调试
 
   ```bash
   rosrun image_view image_view image:=/usb_cam/image_raw
   ```
 
## roslaunch调试
 
```bash
roslaunch usb_cam usb_cam-test.launch
```
 
## 参数说明
 
`usb_cam`配置信息是通过rosparam来进行设置的。
 
|        参数        |    默认值     |                             说明                             | 编程关注度 |
| :----------------: | :-----------: | :----------------------------------------------------------: | :--------: |
|    video_device    | `/dev/video0` |                       设置使用哪部相机                       |   ★★★★★    |
|    image_width     |      640      |                       输出图片像素宽度                       |   ★★★★★    |
|    image_height    |      480      |                       输出图片像素高度                       |   ★★★★★    |
|    pixel_format    |    `mjpeg`    | 像素格式。取值范围: `yuyv`, `uyvy`, `mjpeg`, `yuvmono10`, `rgb24` 建议使用`yuyv` |   ★★★★★    |
|     framerate      |      30       |                  采样率，每秒钟采样30张图片                  |    ★★★     |
|     brightness     |      -1       |                       亮度。取值0~255                        |    ★★★     |
|      contrast      |      -1       |                      对比度。取值0~255                       |    ★★★     |
|     saturation     |      -1       |                      饱和度。取值0~255                       |    ★★★     |
|     sharpness      |      -1       |                       锐度。取值0~255                        |    ★★★     |
|     io_method      |    `mmap`     |               读取方式.`mmap`,`read`,`userptr`               |     ★      |
|     autofocus      |    `false`    |                           自动聚焦                           |     ★      |
|       focus        |      -1       |                         聚焦值.0~255                         |     ★      |
|    autoexposure    |    `false`    |                           自动曝光                           |     ★      |
|      exposure      |      100      |                           曝光值.                            |     ★      |
|        gain        |      -1       |                      曝光增益值。0-100                       |     ★      |
| auto_white_balance |    `false`    |                         自动白平衡。                         |     ★      |
|   white_balance    |     4000      |                          白平衡值。                          |     ★      |
|  camera_frame_id   | `head_camera` |                 标记当前帧是什么设备拍摄的。                 |     ★      |
 
# 图像数据转换
 
## CvBridge介绍
 
![](img/2.png)
 
CvBridge主要解决的问题是将Ros的Image数据与OpenCv的Image数据进行相互转换。
 
**Ros Image to OpenCv Image场景**
 
通常Ros Node和相机硬件进行数据交互，最终拿到的是 Ros Image类型数据。
 
对于这种数据，我们希望通过OpenCv库进行图片数据的操作。但是OpenCv需要的是Mat类型的数据。
 
因此，需要进行数据类型的转换。这种场景主要是需要对图片进行一下业务操作。
 
**OpenCv Image to Ros Image 场景**
 
OpenCv图片操作完成后的数据是Mat类型的，在业务场景中，如果其他节点需要这个数据的话，是需要订阅这种数据的。在Ros中，OpenCV的Mat数据是不可以在节点与节点间进行传输的，要传输只可以采用Ros的Image类型进行传输。此时就需要将OpenCv的Mat数据转换为Ros 的Image类型。
 
##  RosImage to CvMat(c++)
 
**依赖配置**
 
1. package.xml配置
 
   ```xml
     <build_depend>sensor_msgs</build_depend>
     <build_export_depend>sensor_msgs</build_export_depend>
     <exec_depend>sensor_msgs</exec_depend>
   
     <build_depend>cv_bridge</build_depend>
     <build_export_depend>cv_bridge</build_export_depend>
     <exec_depend>cv_bridge</exec_depend>
   
     <build_depend>image_transport</build_depend>
     <build_export_depend>image_transport</build_export_depend>
     <exec_depend>image_transport</exec_depend>
   ```
 
2. CMakeLists.txt配置
 
   ```cmake
   find_package(catkin REQUIRED COMPONENTS
       roscpp
       rosmsg
       rospy
   
       sensor_msgs
       cv_bridge
       image_transport
   )
   ```
 
3. 引入opencv库
 
   ```cmake
   find_package(OpenCV REQUIRED)
   ```
 
4. 添加链接库
 
   ```cmake
   target_link_libraries(image_subscriber
       ${catkin_LIBRARIES}
       ${OpenCV_LIBS}
   )
   ```
 
**转换代码**
 
1. 引入头
 
   ```c++
   #include <image_transport/image_transport.h>
   #include <cv_bridge/cv_bridge.h>
   #include <sensor_msgs/image_encodings.h>
   #include <opencv2/imgproc/imgproc.hpp>
   #include <opencv2/highgui/highgui.hpp>
   #include "sensor_msgs/Image.h"
   ```
 
2. 转换逻辑
 
   ```c++
   void topicCallback(const sensor_msgs::ImageConstPtr &msg) {
     const cv_bridge::CvImageConstPtr &ptr = cv_bridge::toCvShare(msg);
     cv::Mat mat = ptr->image;
     ...
   }
   ```
   
   
   
##############################
设置 接收的相机 可接收奥比中光 
/home/sk/workspas/demo_ur/src/usb_cam/launch/usb_cam-test.launch  第3行,改摄像机  /dev/video0
    
/home/sk/workspas/demo_ur/src/usb_cam/nodes/usb_cam_node.cpp  第92行,改摄像机     /dev/video0

topicName = '/usb_cam/image_raw' 接收topic图像消息
 发送图像节点
 rosrun usb_cam usb_cam_node
 
#include <cv_bridge/cv_bridge.h>
#include <sensor_msgs/Image.h>
  //msg转opencv mat图像
  const cv_bridge::CvImageConstPtr &ptr = cv_bridge::toCvShare(image,"bgr8");
  cv::Mat mat = ptr->image;

  //Mat转msg  传递处理之后的Mat
  cv_bridge::CvImage newImage;
  newImage.header.seq = ++seq;
  newImage.header.stamp = ros::Time::now();
  newImage.image = mat;
  newImage.encoding = "bgr8";
  //转opencv转数据msg传输
  const sensor_msgs::ImagePtr &image_msg = newImage.toImageMsg();
    
