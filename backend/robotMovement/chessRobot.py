import time
from configparser import ConfigParser

from robotMovement.chessCoordinates import ChessCoordinates
from xarm.wrapper import XArmAPI


class ChessRobot:
    def __init__(self):
        self.piece_height = 45
        self.parser = ConfigParser()
        self.parser.read('robotMovement/robot.conf')
        self.arm = XArmAPI(self.parser.get('xArm', 'ip'))
        self.taken = []
        self.cc = ChessCoordinates()
        self.arm.register_error_warn_changed_callback(callback=self.callback_error_warn_changed)
        # Due to a bug in the xArm SDK, not resetting to the correct zero position upon reset(), 
        # we have to compensate for this by adding the difference between the real zero position and the start position
        self.zero_position = [87, 0, 51.2]
        self.start_position = None
        self.initialize()
        
    
    def callback_error_warn_changed(self, data):
        if data['error_code'] == 22: # 22 = self collision
            self.arm.reset(wait=True)
            self.start_position = self.arm.position
        if data['error_code'] == 31: # 31 = collision
            self.arm.motion_enable(enable=True)
            self.arm.set_mode(0)
            self.arm.set_state(state=0)
            self.moving(100, self.arm.position[1], 200)

    def initialize(self):
        self.arm.connect()
        self.arm.motion_enable(enable=True)
        self.arm.set_mode(0)
        self.arm.set_state(state=0)
        self.arm.set_collision_sensitivity(3)
        time.sleep(1)
        self.arm.reset(wait=True)
        self.start_position = self.arm.position

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

    def moving(self, x, y, z, speed=110):
        # Calculating the correct position according to physical zero position
        x_diff = -self.zero_position[0] + self.start_position[0]
        y_diff = -self.zero_position[1] + self.start_position[1]
        z_diff = -self.zero_position[2] + self.start_position[2]
        x = x + x_diff
        y = y + y_diff
        z = z + z_diff
        self.arm.set_position(x, y, z, roll=-180, pitch=0, yaw=0, speed=40, wait=True)
    
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














