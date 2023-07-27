import time
from xarm.wrapper import XArmAPI
from configparser import ConfigParser
from chessCoordinates import ChessCoordinates

class ChessRobot:
    def __init__(self):
        self.piece_height = {
            "p": 67, #pawn
            "n": 85, #knight
            "b": 83, #bishop
            "r": 87, #rook
            "q": 95, #queen
            "k": 103 #king
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

    def movePiece(self, start_x, start_y, x, y, piece):
        self.moving(100, 0, 200)

        self.moving(start_x, start_y, 200)
        self.moving(start_x, start_y, self.piece_height[piece], 80)
        
        self.arm.close_lite6_gripper()
        time.sleep(1)
        self.moving(start_x, start_y, 200)

        self.moving(x, y, 200)
        self.moving(x, y, self.piece_height[piece], 80)
        
        self.arm.open_lite6_gripper()
        time.sleep(1)
        self.arm.stop_lite6_gripper()
        self.moving(x, y, 200)
        self.moving(100, 0, 200)

    def doMove(self, move, piece):
        move_from, move_to = move[:len(move)//2], move[len(move)//2:]
        x_from, y_from = self.cc.chess_to_robot(move_from)
        x_to, y_to = self.cc.chess_to_robot(move_to)
        self.movePiece(x_from, y_from, x_to, y_to, piece)

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
    cr.doMove("a1a3", "r")


