//
// Created by wt on 2020/8/28.
//

#ifndef URDRIVERCPP_URSCRIPT_H
#define URDRIVERCPP_URSCRIPT_H

#include <QString>
class URScript {
public:
    URScript();

    ~URScript();
    //加载movej脚本
    QString loadMovejScript(double joints[6],double a,double v);
    //加载movel脚本
    QString loadMovelScript(double pose[6],double a,double v);
    //加载movep脚本
    QString loadMovepScript(double pose[6],double a,double v);

};


#endif //URDRIVERCPP_URSCRIPT_H
