from visualModule.visual_module import VisualModule 
from visualModule.stream import Stream
from visualModule.coordinate_definer import CoordinateDefiner
import cv2

def start_game():
    # Start calibration
    stream = Stream()
    vm = VisualModule()
    img = stream.start_stream()
    ret, H = vm.findTransformation(img)
    if not ret:
        return
    img = vm.applyHomography(img, H)
    img = vm.drawQuadrants(img)
    cv2.imshow("Before rotation", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Rotate the image
    cd = CoordinateDefiner()
    theta = cd.define_places(3, 4)
    rotMat = vm.findRotation(theta)
    img = vm.applyRotation(img, rotMat)
    cv2.imshow("After rotation", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    start_game()
