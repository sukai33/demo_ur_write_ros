#!/bin/bash
catkin_make
if [[ $? != 0 ]]; then
echo 'catkin_make :error'
else
echo 'catkin_make :ok'
source devel/setup.bash
echo 'source devel/setup.bash :ok'
fi
