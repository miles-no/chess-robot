from visualModule.visual_module import VisualModule 
from visualModule.stream import Stream
from visualModule.coordinate_definer import CoordinateDefiner
import cv2

stream = Stream()
vm = VisualModule()

def start_game():
    # Start calibration
    board = stream.start_stream()
    ret, H = vm.findTransformation(board)
    if not ret:
        return
    empty_board = vm.applyHomography(board, H)
    stream.show_photo(empty_board, "Empty board")

    # Add the pieces

    # Take a photo and rotate it
    preState = rotated_image(3, 4, H)
    cv2.imshow("PreState", preState)
    cv2.imwrite("PreState.jpg", preState)
    stream.close_window() 

    # Player moves a piece

    # Take a photo
    currState = rotated_image(3, 4, H)
    cv2.imshow("CurrState", currState)
    cv2.imwrite("CurrState.jpg", currState)
    stream.close_window() 


def rotated_image(ro1, ro2, H):
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
    theta = cd.define_places(ro1, ro2) # TODO: Change this to the user input
    rotMat = vm.findRotation(theta)
    preState = vm.applyRotation(clean_start_state, rotMat)
    return preState


if __name__ == "__main__":
    start_game()
