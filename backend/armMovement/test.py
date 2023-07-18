#!/usr/bin/env python3
# Software License Agreement (BSD License)
#
# Copyright (c) 2019, UFACTORY, Inc.
# All rights reserved.
#
# Author: Vinman <vinman.wen@ufactory.cc> <vinman.cub@gmail.com>

"""
Description: Move line(linear motion)
"""

import os
import sys
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from xarm.wrapper import XArmAPI

ip = "192.168.1.111"
#######################################################
"""
Just for test example
"""
if len(sys.argv) >= 2: 
    ip = sys.argv[1]
else:
    try:
        from configparser import ConfigParser
        parser = ConfigParser()
        parser.read('../robot.conf')
        ip = parser.get('xArm', 'ip')
    except:
        ip = "192.168.1.111"
########################################################


arm = XArmAPI(ip)
arm.motion_enable(enable=True)
arm.set_mode(0)
arm.set_state(state=0)
time.sleep(2)
arm.reset(wait=True)

arm.set_position(x=300, y=100, z=100, roll=-180, pitch=0, yaw=0, speed=100, wait=True)
print(arm.get_position(), arm.get_position(is_radian=True))
arm.set_position(x=300, y=100, z=43, roll=-180, pitch=0, yaw=0, speed=100, wait=True)
print(arm.get_position(), arm.get_position(is_radian=True))
time.sleep(1)
arm.close_lite6_gripper()
time.sleep(2)
arm.set_position(x=300, y=100, z=200, roll=-180, pitch=0, yaw=0, speed=100, wait=True)
print(arm.get_position(), arm.get_position(is_radian=True))
arm.set_position(x=300, y=0, z=43, roll=-180, pitch=0, yaw=0, speed=100, wait=True)
print(arm.get_position(), arm.get_position(is_radian=True))
time.sleep(2)
arm.open_lite6_gripper()
time.sleep(1)
arm.stop_lite6_gripper()
time.sleep(1)
arm.set_position(x=100, y=0, z=200, roll=-180, pitch=0, yaw=0, speed=100, wait=True)
print(arm.get_position(), arm.get_position(is_radian=True))
time.sleep(1)
arm.reset(wait=True)
arm.disconnect()





