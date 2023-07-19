class ChessRobot:
    def __init__(self):
        self.piece_height = {
            1: 10, #pawn
            2: 7, #knight
            3: 7, #bishop
            4: 4, #rook
            5: 2, #queen
            6: 0 #king
        }