import time
from xarm.wrapper import XArmAPI
from configparser import ConfigParser
from chessCoordinates import ChessCoordinates

class ChessRobot:
    def __init__(self):
        self.piece_height = {
            1: 25, #pawn
            2: 40, #knight
            3: 38, #bishop
            4: 35, #rook
            5: 55, #queen
            6: 67 #king
        }
        self.parser = ConfigParser()
        self.parser.read('robot.conf')
        self.arm = XArmAPI(self.parser.get('xArm', 'ip'))
        self.initialize()
    
    def initialize(self):
        self.arm.motion_enable(enable=True)
        self.arm.set_mode(0)
        self.arm.set_state(state=0)
        time.sleep(2)
        self.arm.reset(wait=True)

    def movePiece(self, start_x, start_y, x, y, piece):
        self.moving(100, 0, 150)
        self.moving(start_x, start_y, 150)
        self.moving(start_x, start_y, self.piece_height[piece])
        
        self.arm.close_lite6_gripper()
        time.sleep(1)

        self.moving(start_x, start_y, 150)
        self.moving(x, y, 150)
        self.moving(x, y, self.piece_height[piece])
    
        self.arm.open_lite6_gripper()
        time.sleep(1)
        self.arm.stop_lite6_gripper()
        time.sleep(1)

        self.moving(x, y, 150)
        self.moving(100, 0, 150)

        self.arm.reset(wait=True)

    def doMove(self, move, piece):
        cc = ChessCoordinates()
        move_from, move_to = move[:len(move)//2], move[len(move)//2:]
        x_from, y_from = cc.chess_to_robot(move_from)
        x_to, y_to = cc.chess_to_robot(move_to)
        self.movePiece(x_from, y_from, x_to, y_to, piece)
    
    def moving(self, x, y, z):
        self.arm.set_position(x=x, y=y, z=z, roll=-180, pitch=0, yaw=0,speed=50, wait=True)
        time.sleep(1)
    
    def disconnect(self):
        self.arm.disconnect()


if __name__ == "__main__":
    piece = 5
    cr = ChessRobot()
    cr.doMove("d1h5", 5)

