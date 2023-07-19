import os
import sys
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from xarm.wrapper import XArmAPI
from chessRobot import ChessRobot
from configparser import ConfigParser
parser = ConfigParser()
parser.read('robot.conf')
ip = parser.get('xArm', 'ip')

cr = ChessRobot()

#Initialize robot
arm = XArmAPI(ip)
arm.motion_enable(enable=True)
arm.set_mode(0)
arm.set_state(state=0)
time.sleep(2)
#Reset to start position(Zero position)
arm.reset(wait=True)

piece = 5
print(cr.piece_height[piece])

# #Move robot
# arm.set_position(x=300, y=100, z=100, roll=-180, pitch=0, yaw=0, speed=100, wait=True)
# print(arm.get_position(), arm.get_position(is_radian=True))
# arm.set_position(x=300, y=100, z=cr.piece_height[piece], roll=-180, pitch=0, yaw=0, speed=100, wait=True) #43 -king 65
# print(arm.get_position(), arm.get_position(is_radian=True))
# time.sleep(1)
# #Close gripper
# arm.close_lite6_gripper()
# time.sleep(2)
# arm.set_position(x=300, y=100, z=200, roll=-180, pitch=0, yaw=0, speed=100, wait=True)
# print(arm.get_position(), arm.get_position(is_radian=True))
# arm.set_position(x=300, y=0, z=cr.piece_height[piece], roll=-180, pitch=0, yaw=0, speed=100, wait=True)
# print(arm.get_position(), arm.get_position(is_radian=True))
# time.sleep(2)
# #Open gripper
# arm.open_lite6_gripper()
# time.sleep(1)
# #Stop gripper engine
# arm.stop_lite6_gripper()
# time.sleep(1)
# #Inclination before going back to starting position
# arm.set_position(x=100, y=0, z=200, roll=-180, pitch=0, yaw=0, speed=100, wait=True)
# print(arm.get_position(), arm.get_position(is_radian=True))
# time.sleep(1)
# # #Go back to start position
# arm.reset(wait=True)
# arm.disconnect()
def movePiece(initialX, initialY, x, y, piece):
    arm.set_position(x=100, y=0, z=150, roll=-180, pitch=0, yaw=0,speed=50, wait=True)
    time.sleep(1)
    arm.set_position(x=initialX, y=initialY, z=150, roll=-180, pitch=0, yaw=0,speed=50, wait=True)
    time.sleep(1)
    arm.set_position(x=initialX, y=initialY, z=cr.piece_height[piece], roll=-180, pitch=0, yaw=0, speed=50,wait=True)
    time.sleep(1)
    arm.close_lite6_gripper()
    time.sleep(1)
    arm.set_position(x=initialX, y=initialY, z=150, roll=-180, pitch=0, yaw=0, speed=50,wait=True)
    time.sleep(1)
    arm.set_position(x=x, y=y, z=150, roll=-180, pitch=0, yaw=0, speed=50,wait=True)
    time.sleep(1)
    arm.set_position(x=x, y=y, z=cr.piece_height[piece], roll=-180, pitch=0, yaw=0, speed=50,wait=True)
    time.sleep(1)
    arm.open_lite6_gripper()
    time.sleep(1)
    arm.stop_lite6_gripper()
    time.sleep(1)
    arm.set_position(x=x, y=y, z=150, roll=-180, pitch=0, yaw=0, speed=50, wait=True)
    time.sleep(1)
    arm.set_position(x=100, y=0, z=150, roll=-180, pitch=0, yaw=0,speed=80, wait=True)
    time.sleep(1)
    arm.reset(wait=True)
    
movePiece(150, 121, 402, 121, piece) #a1 to a8
arm.disconnect()





