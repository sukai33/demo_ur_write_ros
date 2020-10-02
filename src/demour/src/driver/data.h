//
// Created by wt on 2020/6/4.
//

#ifndef URDRIVERCPP_DATA_H
#define URDRIVERCPP_DATA_H

//连接上机械臂，机械臂返回的数据
struct URData{
    int MsgSize;//121
    double Time;
    double q_target[6];
    double qd_target[6];
    double qdd_target[6];
    double I_target[6];
    double M_target[6];
    //当前关节角度
    double q_actual[6];
    double qd_actual[6];//关节角度
    double I_actual[6];
    double I_control[6];
    //当前工具位置
    double Tool_vector_actual[6];
    double TCP_speed_actual[6];
    double TCP_force[6];
    double Tool_vector_target[6];
    double TCP_speed_target[6];
    double Digital_input_bits;
    double Motor_temperatures[6];
    double Controller_Timer;
    double Test_value;
    double Robot_Mode;
    double Joint_Modes[6];
    double Safety_Mode;
    double Buffer1[6];
    double Tool_Accelerometer_values[3];
    double Buffer2[6];
    double Speed_scaling;
    double Linear_momentum_norm;
    double Buffer3;
    double Buffer4;
    double V_main;
    double V_robot;
    double I_robot;
    double V_actual[6];
    double Digital_outputs;
    //机械臂状态：1 空闲  2 工作
    double Program_state;
    double Elbow_position[3];
    double Elbow_velocity[3];
};

//枚举
enum MOVETYPE{
    MOVEJ,
    MOVEL,
    MOVEP
};

//指令结构体
struct Instruction{
    MOVETYPE movetype;
    double data[6];
    double a;
    double v;
};

#endif //URDRIVERCPP_DATA_H
