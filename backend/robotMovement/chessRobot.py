import math
import time
from xarm.wrapper import XArmAPI
from configparser import ConfigParser
from chessCoordinates import ChessCoordinates

class ChessRobot:
    def __init__(self):
        self.piece_height = {
            "p": 25, #pawn
            "n": 38, #knight
            "b": 38, #bishop
            "r": 35, #rook
            "q": 55, #queen
            "k": 67 #king
        }
        self.parser = ConfigParser()
        self.parser.read('robot.conf')
        self.arm = XArmAPI(self.parser.get('xArm', 'ip'))
        self.initialize()
        self.taken = []
    
    def initialize(self):
        self.arm.motion_enable(enable=True)
        self.arm.set_mode(0)
        self.arm.set_state(state=0)
        self.arm.set_collision_sensitivity(5)
        time.sleep(2)
        self.arm.reset(wait=True)

    def movePiece(self, start_x, start_y, x, y, piece, king_position=False):
        self.moving(100, 0, 150, 100)
        self.moving(start_x, start_y, 150, 100)
        if king_position:
            print("King on the side")
            self.rotate_robot()
        self.moving(start_x, start_y, self.piece_height[piece])
        
        time.sleep(1)
        self.arm.close_lite6_gripper()
        
        self.moving(start_x, start_y, 150, 80)
        self.moving(x, y, 150, 100)
        self.moving(x, y, self.piece_height[piece])

        time.sleep(1)
        self.arm.open_lite6_gripper()
        time.sleep(1)
        self.arm.stop_lite6_gripper()

        self.moving(x, y, 150, 80)
        self.moving(100, 0, 150, 100)

    def doMove(self, move, piece, king_position=False):
        cc = ChessCoordinates()
        move_from, move_to = move[:len(move)//2], move[len(move)//2:]
        start_x, start_y = cc.chess_to_robot(move_from)
        #x_to, y_to = cc.chess_to_robot(move_to)
        self.arm.set_position(x=100, y=0, z=150, roll=-180, pitch=0, yaw=0,speed=100, wait=True)
        self.arm.set_position(x=start_x, y=start_y, z=150, roll=-180, pitch=0, yaw=0,speed=100, wait=True)
        self.arm.set_position(x=start_x, y=start_y, z=150, roll=-180, pitch=0, yaw=0,speed=50, wait=True)


        #self.arm.set_servo_angle(servo_id=6, angle=90, is_radian=False, wait=True)
 
        self.arm.set_position(x=start_x, y=start_y, z=self.piece_height[piece], roll=-180, pitch=0, yaw=0, speed=80, wait=True)
    

        # self.movePiece(x_from, y_from, x_to, y_to, piece, king_position)
        # self.arm.reset(wait=True)
    
    def moving(self, x, y, z, speed=50):
        time.sleep(1)
        self.arm.set_position(x=x, y=y, z=z, roll=-180, pitch=0, yaw=0,speed=speed, wait=True)
    
    def disconnect(self):
        self.arm.disconnect()

    def reset(self):
        self.arm.reset(wait=True)

    # Move the piece that have been taken outside 
    def move_taken(self, move_from, piece):
        cc = ChessCoordinates()
        x_from, y_from = cc.chess_to_robot(move_from)
        self.taken.append(piece)
        if len(self.taken) < 7:
            x = 130 + (len(self.taken)-1)*40
            y = 160
        else:
            x = 130 + (len(self.taken)-7)*40
            y = -162
        self.movePiece(x_from, y_from, x, y, piece)
    
    def rotate_robot(self):
        self.arm.set_servo_angle(servo_id=6, angle=90, is_radian=False, wait=False)
        # self.arm.set_position(x=200, y=0, z=200, roll=-180, pitch=0, yaw=0,speed=80, wait=True


if __name__ == "__main__":
    cr = ChessRobot()
    #cr.doMove("e2e4", "p")
    cr.doMove("f1d3", "b", True)
    








