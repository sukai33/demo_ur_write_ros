//
// Created by sk on 2020/8/31.
//

#include "PaintWidget.h"
#include "Type.cpp"
PaintWidget::PaintWidget() {
}
//清理画板
void PaintWidget::clear(){
    points.clear();
    this->update();
}




void PaintWidget::mousePressEvent(QMouseEvent *event){
    double x = (double)event->x();
    double y = (double)event->y();
    double z = 30;
    double aubo_z = -0.004374;
  // map<string, int> point(pair<string, int>("x",x),pair<string, int>("y",y),pair<string, int>("z",z),pair<string, int>("typt",0));
    map<string, double> point;
    point.insert({"x",x});
    point.insert({"y",y});
    point.insert({"z",z});
    point.insert({"aubo_z",aubo_z});
    point.insert({"type",0});
    points.push_back(point);
    //cout<<"鼠标按下:"<<"X: "<<x<<" Y: "<<y<<endl;
    this->update();
}
//鼠标移动
void PaintWidget::mouseMoveEvent(QMouseEvent *event){
    double x = (double)event->x();
    double y = (double)event->y();
    double z = 30;
    double aubo_z = -0.002374;
    map<string, double> point;
    point.insert({"x",x});
    point.insert({"y",y});
    point.insert({"z",z});
    point.insert({"aubo_z",aubo_z});
    point.insert({"type",1});
    points.push_back(point);
    //cout<<"鼠标移动:"<<"X: "<<x<<" Y: "<<y<<endl;
    this->update();
}
// 鼠标松开
void PaintWidget::mouseReleaseEvent(QMouseEvent *event){
    double x = (double)event->x();
    double y = (double)event->y();
    double z=45;
    double aubo_z = 0.00906;
    map<string, double> point;
    point.insert({"x",x});
    point.insert({"y",y});
    point.insert({"z",z});
    point.insert({"aubo_z",aubo_z});
    point.insert({"type",2});
    points.push_back(point);
    //cout<<"鼠标松开:"<<"X: "<<x<<" Y: "<<y<<endl;
    this->update();
}
// 制事件
void PaintWidget::paintEvent(QPaintEvent *event){
   if (points.empty()){
       return;
   }
//// 创建画家
   QPainter  painter(this);
////创建画笔
   QPen pen;
// 设置画笔颜色
    pen.setColor(QColor(255,0,0));
//设置画笔
    painter.setPen(pen);
    //绘制已经走过的点  10个点,如何绘制
    map<string ,double> startPoint = points[0];
    for (int i = 0; i < points.size() ; ++i) {
        //获取结束的点
        map<string ,double>  endPoint = points[i];
        // 绘制
        if (startPoint["type"]!=2){
            painter.drawLine(startPoint["x"], startPoint["y"], endPoint["x"], endPoint["y"]);
        }
        // 修改起点
        startPoint = endPoint;
    }




}
vector<map<string ,double>> PaintWidget::getPoints(){
    return points;
}
PaintWidget::~PaintWidget() {


}
