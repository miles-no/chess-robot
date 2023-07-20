import time
from xarm.wrapper import XArmAPI
from configparser import ConfigParser
from robotMovement.chessCoordinates import ChessCoordinates

class ChessRobot:
    def __init__(self):
        self.piece_height = {
            "p": 25, #pawn
            "n": 40, #knight
            "b": 38, #bishop
            "r": 35, #rook
            "q": 55, #queen
            "k": 67 #king
        }
        self.parser = ConfigParser()
        self.parser.read('robotMovement/robot.conf')
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

    def movePiece(self, start_x, start_y, x, y, piece):
        self.moving(100, 0, 150, 80)
        self.moving(start_x, start_y, 150, 80)
        self.moving(start_x, start_y, self.piece_height[piece])
        
        self.arm.close_lite6_gripper()
        time.sleep(1)

        self.moving(start_x, start_y, 150)
        self.moving(x, y, 150, 80)
        self.moving(x, y, self.piece_height[piece])
    
        self.arm.open_lite6_gripper()
        time.sleep(1)
        self.arm.stop_lite6_gripper()
        time.sleep(1)

        self.moving(x, y, 150)
        self.moving(100, 0, 150, 80)

    def doMove(self, move, piece):
        cc = ChessCoordinates()
        move_from, move_to = move[:len(move)//2], move[len(move)//2:]
        x_from, y_from = cc.chess_to_robot(move_from)
        x_to, y_to = cc.chess_to_robot(move_to)
        self.movePiece(x_from, y_from, x_to, y_to, piece)
        self.arm.reset(wait=True)
    
    def moving(self, x, y, z, speed=50):
        self.arm.set_position(x=x, y=y, z=z, roll=-180, pitch=0, yaw=0,speed=speed, wait=True)
        time.sleep(1)
    
    def disconnect(self):
        self.arm.disconnect()

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


if __name__ == "__main__":
    cr = ChessRobot()
    cr.doMove("d1h5", "q")

