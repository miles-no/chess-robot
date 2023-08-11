class ChessCoordinates():
    def __init__(self):
        self.tile = 35
        self.a_position_white = {"x": 150, "y": 120}
        self.a_position_black = {"x": 395, "y": -125}

    def chess_to_robot(self, position, color):
        y, number = self.split_strings(position)
        x = number-1
        if color:
            x = self.a_position_white["x"] + x*self.tile
            y = self.a_position_white["y"] - y*self.tile
        else:
            x = self.a_position_black["x"] - x*self.tile
            y = self.a_position_black["y"] + y*self.tile
        return x, y
    
    def split_strings(self, string):
        letter, number = string[:len(string)//2], int(string[len(string)//2:])
        l2n = ord(letter)-97
        return l2n, number
