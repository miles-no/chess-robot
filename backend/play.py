from visualModule.visual_module import VisualModule 
from visualModule.stream import Stream
from visualModule.coordinate_definer import CoordinateDefiner
import cv2

def start_game():
    # Start calibration
    stream = Stream()
    vm = VisualModule()
    board = stream.start_stream()
    ret, H = vm.findTransformation(board)
    if not ret:
        return
    empty_board = vm.applyHomography(board, H)
    stream.show_photo(empty_board, "Empty board")

    # Add the pieces

    # Take a photo
    cap = cv2.VideoCapture(0)
    start_state = stream.take_photo(cap)
    stream.stop_stream(cap)
    stream.show_photo(start_state, "Start state")
    clean_start_state = vm.applyHomography(start_state, H)

    Qstart_state = vm.drawQuadrants(clean_start_state)
    stream.show_photo(Qstart_state, "Before rotation")

    # Rotate the image
    cd = CoordinateDefiner()
    theta = cd.define_places(3, 4) # TODO: Change this to the user input
    rotMat = vm.findRotation(theta)
    preState = vm.applyRotation(Qstart_state, rotMat)
    cv2.imshow("After rotation", preState)
    stream.close_window() 


if __name__ == "__main__":
    start_game()
