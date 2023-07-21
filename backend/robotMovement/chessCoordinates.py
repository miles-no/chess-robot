class ChessCoordinates():
    def __init__(self):
        self.tile = 35
        self.a_position = {"x": 150, "y": 120}

    def chess_to_robot(self, position):
        letter, number = position[:len(position)//2], int(position[len(position)//2:])
        y = ord(letter)-97
        x = number-1
        x = self.a_position["x"] + x*self.tile
        y = self.a_position["y"] - y*self.tile
        return x, y
        
if __name__ == "__main__":
    cc = ChessCoordinates()
    cc.get_piece_position("h1")