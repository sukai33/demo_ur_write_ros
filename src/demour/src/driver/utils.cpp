//
// Created by wt on 2020/6/4.
//

#include "utils.h"
#include <math.h>
#include <memory.h>

void reverseByte(char *p, int size) {
    if (size == 4) {
        //0001
        char tmp = p[0];//*p
        p[0] = p[3];//*(p+3)
        p[3] = tmp;

        tmp = p[1];
        p[1] = p[2];
        p[2] = tmp;
    } else if (size == 8) {
        //10000000
        char tmp = p[0];
        p[0] = p[7];
        p[7] = tmp;


        tmp = p[1];
        p[1] = p[6];
        p[6] = tmp;

        tmp = p[2];
        p[2] = p[5];
        p[5] = tmp;

        tmp = p[3];
        p[3] = p[4];
        p[4] = tmp;
    }
}

bool isClose(Instruction &target, URData &urData) {
    ////机械臂状态：1 空闲  2 工作
//    double d = urData.Program_state;
//    if (d<=1){
//        return true;
//    }else{
//        return false;
//    }

    //目标数据
    double targetData[6];
    memcpy(targetData, target.data, 6 * sizeof(double));
    //当前数据
    double curData[6];
    if (target.movetype == MOVEJ) {
        memcpy(curData, urData.q_actual, 6 * sizeof(double));
    } else if (target.movetype == MOVEL || target.movetype == MOVEP ) {
        memcpy(curData, urData.Tool_vector_actual, 6 * sizeof(double));
    }
    //判断是否足够接近
    double result = variance(target.movetype, targetData, curData);
   // return result < 0.018;
    return result < 0.001;
}

double variance(MOVETYPE movetype, double *targetData, double *curData) {
    double result;
    for (int i = 0; i < 6; ++i) {
        if (movetype == MOVEL && (i == 3 || i == 4 || i == 5)) {
            result += pow(abs(targetData[i]) - abs(curData[i]), 2);
        } else if (movetype == MOVEP && (i == 3 || i == 4 || i == 5)) {
            result += pow(abs(targetData[i]) - abs(curData[i]), 2);
        }else {
            result += pow(targetData[i] - curData[i], 2);
        }
    }
    return sqrt(result);
}


