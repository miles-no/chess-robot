class ChessCoordinates():
    def __init__(self):
        self.tile = 36
        self.y_coordinates = {"a": 121, "h": -123}
        self.x_coordinate = 150
        self.letters = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 3, "f": 2, "g": 1, "h": 0}
        self.positive_side = ["a", "b", "c", "d"]

    def chess_to_robot(self, position):
        letter, number = position[:len(position)//2], int(position[len(position)//2:])
        y = self.letters[letter]
        x = number-1
        x = self.x_coordinate + x*self.tile
        if letter in self.positive_side:
            y = self.y_coordinates["a"] - y*self.tile
        else:
            y = self.y_coordinates["h"] + y*self.tile
        return x, y
        
if __name__ == "__main__":
    cc = ChessCoordinates()
    cc.get_piece_position("h1")