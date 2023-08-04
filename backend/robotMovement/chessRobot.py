import time
from xarm.wrapper import XArmAPI
from configparser import ConfigParser
from chessCoordinates import ChessCoordinates

class ChessRobot:
    def __init__(self):
        self.piece_height = 45
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

    def movePiece(self, start_x, start_y, x, y):
        self.moving(100, 0, 110)

        self.moving(start_x, start_y, 110)
        self.moving(start_x, start_y, 80, 80)
        self.moving(start_x, start_y, self.piece_height, 30)
        
        self.arm.close_lite6_gripper()
        time.sleep(1)
        self.moving(start_x, start_y, 110)

        self.moving(x, y, 110)
        self.moving(x, y, self.piece_height, 80)
        
        self.arm.open_lite6_gripper()
        time.sleep(1)
        self.arm.stop_lite6_gripper()
        self.moving(x, y, 110)
        self.moving(100, 0, 110)

    def doMove(self, move):
        move_from, move_to = move[:len(move)//2], move[len(move)//2:]
        x_from, y_from = self.cc.chess_to_robot(move_from)
        x_to, y_to = self.cc.chess_to_robot(move_to)
        self.movePiece(x_from, y_from, x_to, y_to)

    def moving(self, x, y, z, speed=110, yaw=0):
        self.arm.set_position(x=x, y=y, z=z, roll=-180, pitch=0, yaw=yaw, speed=speed, wait=True)
    
    def disconnect(self):
        self.arm.disconnect()

    def reset(self):
        self.arm.reset(wait=True)

    # Move the piece that have been taken outside 
    def move_taken(self, move_from, piece):
        x_from, y_from = self.cc.chess_to_robot(move_from)
        self.taken.append(piece)
        if len(self.taken) < 8:
            x = 130 + (len(self.taken)-1)*40
            y = 160
        else:
            x = 130 + (len(self.taken)-8)*40
            y = -162
        self.movePiece(x_from, y_from, x, y)


if __name__ == "__main__":
    cr = ChessRobot()
    cr.doMove("a8a6")
    # cr.doMove("b1a3", "n")
    # cr.doMove("c1g5", "b")
    # cr.doMove("b2b4", "p")
    # cr.doMove("d1d6", "q")
    # cr.doMove("c2c4", "p")
    # cr.doMove("a1a2", "r")
    # cr.doMove("f1f3", "p")
    # cr.doMove("e1f1", "k")
    # cr.doMove("g5f6", "b")
    # cr.doMove("f1f2", "k")
    # cr.doMove("a3b5", "n")
    # cr.doMove("a2a6", "r")














