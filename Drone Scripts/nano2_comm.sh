#!/bin/bash
export ROS_IP=192.168.1.200
export ROS_MASTER_URI=http://192.168.1.150:11311
sleep 2
rosrun comm drone.py
sleep 2
#sleep 2
#./check_connection.py
