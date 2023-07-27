class ChessCoordinates():
    def __init__(self):
        self.tile = 35
        self.a_position = {"x": 150, "y": 120}

    def chess_to_robot(self, position):
        y, number = self.split_strings(position)
        x = number-1
        x = self.a_position["x"] + x*self.tile
        y = self.a_position["y"] - y*self.tile
        return x, y
    
    def split_strings(self, string):
        letter, number = string[:len(string)//2], int(string[len(string)//2:])
        l2n = ord(letter)-97
        return l2n, number

if __name__ == "__main__":
    cc = ChessCoordinates()
    cc.get_piece_position("h1")