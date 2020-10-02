//
// Created by wt on 2020/6/4.
//

#ifndef URDRIVERCPP_UTILS_H
#define URDRIVERCPP_UTILS_H
#include "data.h"
#include <math.h>
/**
 * 大小端转换  交换字节数据
 * @param p 交换开始的数据指针
 * @param size 交换长度
 */
void reverseByte(char *p,int size);

//是否足够接近
bool isClose(Instruction& target,URData &urData);

double variance(MOVETYPE movetype,double targetData[6],double curData[6]);

#endif //URDRIVERCPP_UTILS_H
