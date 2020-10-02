//
// Created by wt on 2020/8/28.
//

#include "URScript.h"

URScript::URScript() {

}

URScript::~URScript() {

}

QString URScript::loadMovejScript(double *joints, double a, double v) {
    //'movej([90,80], a=1.4, v=1.05, t=0, r=0)'
    QString msg{"movej(["};
    for (int i = 0; i < 6; ++i) {
        msg += QString::number(joints[i]);
        if (i != 5) {
            msg += ",";
        }
    }
    msg += "], a=";
    msg += QString::number(a);
    msg += ", v=";
    msg += QString::number(v);
    //最后面  必要要有换行符
    msg+=", t=0, r=0)\n";
    return msg;
}

QString URScript::loadMovelScript(double *pose, double a, double v) {
    //movel(pose, a=1.2, v=0.25, t=0, r=0)
    QString msg{"movel(p["};
    for (int i = 0; i < 6; ++i) {
        msg += QString::number(pose[i]);
        if (i != 5) {
            msg += ",";
        }
    }
    msg += "], a=";
    msg += QString::number(a);
    msg += ", v=";
    msg += QString::number(v);
    //最后面  必要要有换行符
    msg+=", t=0, r=0)\n";
    return msg;
}

//movep(p[-0.054312,-0.426565,0.03025,3.1401,-0.0002,0.0], a=1.2, v=0.25, r=0)
//movep(p[-0.023248,-0.410077,0.04555,3.1401,-0.0002,0.0], a=1.2, v=0.25, r=0)
QString URScript::loadMovepScript(double *pose, double a, double v) {
    //movep(p[-0.023248,-0.410077,0.04555,3.1401,-0.0002,0.0], a=1.2, v=0.25, r=0)
    printf("=====================movep=======================");
    QString msg{"movep(p["};
    for (int i = 0; i < 6; ++i) {
        msg += QString::number(pose[i]);
        if (i != 5) {
            msg += ",";
        }
    }
    msg += "], a=";
    msg += QString::number(a);
    msg += ", v=";
    msg += QString::number(v);
    //最后面  必要要有换行符
    msg+=", r=0.0)\n";
    return msg;
}
