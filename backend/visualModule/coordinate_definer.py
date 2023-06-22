class CoordinateDefiner():
    def __init__(self):
        self.rotation = {
            (1,2): 0,
            (2,4): 90,
            (3,4): 180,
            (1,3): 270,
        }
    
    # Define the piece color to play with
    def define_piece_choice(self, choice):
        if choice == 1:
            return "white"
        else:
            return "black"
    
    # Define the places of the pieces where the user start
    def define_places(self, x, y):
        if (x, y) in self.rotation:
            return self.rotation[(x, y)]
        elif (y, x) in self.rotation:
            return self.rotation[(y, x)]
        return -1


if __name__ == "__main__":
    coordinate_definer = CoordinateDefiner()
    color_choice = int(input("Define the piece color to play with (0 for black and 1 for white): "))
    start_position = input("Define the places of the pieces where you start (e.g. 1,2): ")
    start_position = start_position.split(",")
    start_position = [eval(i) for i in start_position]
    print(coordinate_definer.define_piece_choice(color_choice))
    print(coordinate_definer.define_places(start_position[0], start_position[1]))
    