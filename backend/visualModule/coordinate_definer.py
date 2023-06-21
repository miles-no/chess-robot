class CoordinateDefiner():
    def __init__(self):
        pass
    
    # Define the piece color to play with
    def define_piece_choice(self, choice):
        if choice == 1:
            return "white"
        else:
            return "black"
    
    # Define the places of the pieces where the user start
    def define_places(self, x, y):
        return f"Chosen corners: {x}, {y}"


if __name__ == "__main__":
    coordinate_definer = CoordinateDefiner()
    color_choice = int(input("Define the piece color to play with (0 for black and 1 for white): "))
    start_position = input("Define the places of the pieces where you start (e.g. 1,2): ")
    start_position = start_position.split(",")
    start_position = [eval(i) for i in start_position]
    print(coordinate_definer.define_piece_choice(color_choice))
    print(coordinate_definer.define_places(start_position[0], start_position[1]))
    