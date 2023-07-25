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
        self.cc = ChessCoordinates()
    
    def initialize(self):
        self.arm.motion_enable(enable=True)
        self.arm.set_mode(0)
        self.arm.set_state(state=0)
        self.arm.set_collision_sensitivity(5)
        time.sleep(2)
        self.arm.reset(wait=True)

    def movePiece(self, start_x, start_y, x, y, piece, move, king_position=None):
        self.moving(100, 0, 150)

        if self.cc.king_on_side_lift(king_position, move):
            self.moving(start_x, start_y, 150, yaw=90)
            self.moving(start_x, start_y, self.piece_height[piece], 80, yaw=90)
        else:
            self.moving(start_x, start_y, 150)
            self.moving(start_x, start_y, self.piece_height[piece], 80)
        
        self.arm.close_lite6_gripper()
        time.sleep(1)
        self.moving(start_x, start_y, 150)

        if self.cc.king_on_side_down(king_position, move):
            self.moving(x, y, 150, yaw=90)
            self.moving(x, y, self.piece_height[piece], 80, yaw=90)
        else:
            self.moving(x, y, 150)
            self.moving(x, y, self.piece_height[piece], 80)

        self.arm.open_lite6_gripper()
        time.sleep(1)
        self.arm.stop_lite6_gripper()

        self.moving(x, y, 150)
        self.moving(100, 0, 150)

    def doMove(self, move, piece, king_position=None):
        move_from, move_to = move[:len(move)//2], move[len(move)//2:]
        x_from, y_from = self.cc.chess_to_robot(move_from)
        x_to, y_to = self.cc.chess_to_robot(move_to)
        self.movePiece(x_from, y_from, x_to, y_to, piece, move, king_position)
        self.arm.reset(wait=True)
    
    def moving(self, x, y, z, speed=100, yaw=0):
        self.arm.set_position(x=x, y=y, z=z, roll=-180, pitch=0, yaw=yaw, speed=speed, wait=True)
    
    def disconnect(self):
        self.arm.disconnect()

    def reset(self):
        self.arm.reset(wait=True)

    # Move the piece that have been taken outside 
    def move_taken(self, move_from, piece):
        x_from, y_from = self.cc.chess_to_robot(move_from)
        self.taken.append(piece)
        if len(self.taken) < 7:
            x = 130 + (len(self.taken)-1)*40
            y = 160
        else:
            x = 130 + (len(self.taken)-7)*40
            y = -162
        self.movePiece(x_from, y_from, x, y, piece)


if __name__ == "__main__":
    cr = ChessRobot()
    cr.doMove("e2e4", "p")
    cr.doMove("f1d3", "b", "e1")