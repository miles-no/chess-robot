import time
from configparser import ConfigParser

from robotMovement.chessCoordinates import ChessCoordinates
from xarm.wrapper import XArmAPI
import os


class ChessRobot:
    # Magic values
    PIECE_HEIGHT = 45
    SAFE_HEIGHT = 100
    SPEED_MULTIPLIER = 10
    GRIPPER_WAIT_TIME = 0.75
    ZERO_POSITION = [87, 0, 51.2]
    SAFE_POSITION_X = 100
    SAFE_POSITION_Y = 0
    TAKEN_PIECES_START_X = 130
    TAKEN_PIECES_Y_ROW1 = 160
    TAKEN_PIECES_Y_ROW2 = -162
    TAKEN_PIECES_X_SPACING = 40
    TAKEN_PIECES_PER_ROW = 7

    def __init__(self):
        # Initialize chess robot properties
        self.piece_height = self.PIECE_HEIGHT
        self.parser = ConfigParser()
        loc = os.path.dirname(os.path.abspath(__file__))
        print(loc)
        # Read configuration file
        conf = "/".join([loc, "robot.conf"])
        self.parser.read(conf)
        try:
            # Initialize xArm API
            self.arm = XArmAPI(self.parser.get("xArm", "ip"))
            self.taken = []
            self.cc = ChessCoordinates()
            # Register error callback
            self.arm.register_error_warn_changed_callback(
                callback=self.callback_error_warn_changed
            )
            # Set zero position and initialize start position
            self.zero_position = self.ZERO_POSITION
            self.start_position = None
            self.initialize()
        except Exception as e:
            print(f"Error initializing xArm: {e}")
            self.arm = None

    def reset_taken(self):
        self.taken = []

    def callback_error_warn_changed(self, data):
        # Handle self-collision error
        if data["error_code"] == 22:  # 22 = self collision
            self.arm.reset(wait=True)
            self.start_position = self.arm.position
        # Handle collision error
        if data["error_code"] == 31:  # 31 = collision
            self.arm.motion_enable(enable=True)
            self.arm.set_mode(0)
            self.arm.set_state(state=0)
            self.moving(100, self.arm.position[1], 200)

    def initialize(self):
        # Initialize xArm if available
        if self.arm is None:
            print("xArm not initialized. Skipping initialization.")
            return
        try:
            # Connect and configure xArm
            self.arm.connect()
            self.arm.motion_enable(enable=True)
            self.arm.set_mode(0)
            self.arm.set_state(state=0)
            self.arm.set_collision_sensitivity(3)
            time.sleep(1)
            self.arm.reset(wait=True)
            self.start_position = self.arm.position
        except Exception as e:
            print(f"Error during xArm initialization: {e}")
            self.arm = None

    def movePiece(self, start_x, start_y, x, y):
        # Move to a safe starting position
        self.moving(self.SAFE_POSITION_X, self.SAFE_POSITION_Y, self.SAFE_HEIGHT, speed=130 * self.SPEED_MULTIPLIER)

        # Move above the starting position of the piece
        self.moving(start_x, start_y, self.SAFE_HEIGHT, speed=130 * self.SPEED_MULTIPLIER)
        # Lower to the piece height to grab it
        self.moving(start_x, start_y, self.PIECE_HEIGHT, speed=90 * self.SPEED_MULTIPLIER)

        # Close the gripper to grab the piece
        self.arm.close_lite6_gripper()
        time.sleep(self.GRIPPER_WAIT_TIME)  # Wait for gripper to close // Todo: use callback instead
        # Lift the piece up
        self.moving(start_x, start_y, self.SAFE_HEIGHT, speed=130 * self.SPEED_MULTIPLIER)

        # Move above the destination position
        self.moving(x, y, self.SAFE_HEIGHT, speed=130 * self.SPEED_MULTIPLIER)
        # Lower the piece to the board
        self.moving(x, y, self.PIECE_HEIGHT, speed=90 * self.SPEED_MULTIPLIER)

        # Open the gripper to release the piece
        self.arm.open_lite6_gripper()
        time.sleep(self.GRIPPER_WAIT_TIME)  # Wait for gripper to open // Todo: use callback instead
        self.arm.stop_lite6_gripper()
        # Lift the arm up
        self.moving(x, y, self.SAFE_HEIGHT, speed=130 * self.SPEED_MULTIPLIER)
        # Move back to a safe position
        self.moving(self.SAFE_POSITION_X, self.SAFE_POSITION_Y, self.SAFE_HEIGHT, speed=130 * self.SPEED_MULTIPLIER)

    def doMove(self, move, color):
        # Parse move and convert to robot coordinates
        move_from, move_to = move[: len(move) // 2], move[len(move) // 2 :]
        x_from, y_from = self.cc.chess_to_robot(move_from, color)
        x_to, y_to = self.cc.chess_to_robot(move_to, color)
        # Execute the move
        self.movePiece(x_from, y_from, x_to, y_to)

    def moving(self, x, y, z, speed=110 * 4):
        # Calculate the correct position according to physical zero position
        x_diff = -self.zero_position[0] + self.start_position[0]
        y_diff = -self.zero_position[1] + self.start_position[1]
        z_diff = -self.zero_position[2] + self.start_position[2]
        x = x + x_diff
        y = y + y_diff
        z = z + z_diff
        # Move the arm to the calculated position
        self.arm.set_position(
            x, y, z, roll=-180, pitch=0, yaw=0, speed=speed, wait=True
        )

    def disconnect(self):
        self.arm.disconnect()

    def reset(self):
        self.arm.reset(wait=True)

    def move_taken(self, move_from, piece, color):
        # Move a taken piece off the board
        x_from, y_from = self.cc.chess_to_robot(move_from, color)
        self.taken.append(piece)
        # Determine the position to place the taken piece
        if len(self.taken) <= self.TAKEN_PIECES_PER_ROW:
            # First row of taken pieces (0-7 pieces)
            x = self.TAKEN_PIECES_START_X + (len(self.taken) - 1) * self.TAKEN_PIECES_X_SPACING
            y = self.TAKEN_PIECES_Y_ROW1
        else:
            # Second row of taken pieces (8-15 pieces)
            x = self.TAKEN_PIECES_START_X + (len(self.taken) - self.TAKEN_PIECES_PER_ROW - 1) * self.TAKEN_PIECES_X_SPACING
            y = self.TAKEN_PIECES_Y_ROW2
        self.movePiece(x_from, y_from, x, y)

    def reset_board_to_start(self, moves=None):
        """
        Move only misplaced pieces back to their starting positions.
        If a move list is provided, reconstruct the board and move pieces back.
        """
        import chess
        # Start from the initial board
        board = chess.Board()
        # Apply all moves if provided
        if moves:
            for move in moves:
                try:
                    board.push_uci(move)
                except Exception as e:
                    print(f"Invalid move in move list: {move}, error: {e}")

        # Get current and starting piece maps
        current_map = board.piece_map()
        starting_board = chess.Board()
        starting_map = starting_board.piece_map()

        # Build reverse lookup for starting squares by piece type and color
        starting_squares = {}
        for sq, piece in starting_map.items():
            key = (piece.symbol(), piece.color)
            starting_squares.setdefault(key, []).append(sq)

        # Track which starting squares are already correct
        used_starts = {k: [] for k in starting_squares}

        # For each piece on the current board
        for sq, piece in current_map.items():
            key = (piece.symbol(), piece.color)
            # If this piece is already on a correct starting square, skip
            if sq in starting_squares.get(key, []) and sq not in used_starts[key]:
                used_starts[key].append(sq)
                continue  # Already correct, do not move

            possible_starts = starting_squares.get(key, [])
            from_sq = chess.square_name(sq)

            # Special handling for pawns: match file (column)
            if piece.symbol().lower() == 'p':
                from_file = chess.square_file(sq)
                # Find the starting square for this pawn's file
                start_sq = None
                for s in possible_starts:
                    if chess.square_file(s) == from_file and s not in used_starts[key]:
                        start_sq = s
                        break
                if start_sq is not None:
                    to_sq = chess.square_name(start_sq)
                    print(f"Moving {piece.symbol()} from {from_sq} to {to_sq}")
                    self.doMove(from_sq + to_sq, piece.color)
                    used_starts[key].append(start_sq)
                continue

            # For other pieces, use the first available starting square
            for start_sq in possible_starts:
                if start_sq not in used_starts[key]:
                    to_sq = chess.square_name(start_sq)
                    print(f"Moving {piece.symbol()} from {from_sq} to {to_sq}")
                    self.doMove(from_sq + to_sq, piece.color)
                    used_starts[key].append(start_sq)
                    break

        print("Board reset to starting position (only misplaced pieces moved).")

    def movePieceToSquare(self, from_square, to_square, color=True):
        """
        Move a piece from one square to another using the robot.
        """
        print(f"Moving piece from {from_square} to {to_square}")
        self.doMove(from_square + to_square, color)
