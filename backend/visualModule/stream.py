import cv2
from visualModule.visual_module import VisualModule

class Stream():
    def __init__(self):
        self.vm = VisualModule()

    def start_stream(self):
        cap = cv2.VideoCapture(0)
        currentFrame = 0
        while(True):
            # Capture frame-by-frame
            _, frame = cap.read()
            
            cv2.imshow('frame',frame)

            img = self.take_photo(cap)

            if self.vm.patternRecognizer(img) or cv2.waitKey(1) & 0xFF == ord('q'):
                self.stop_stream(cap)
                break

            # To stop duplicate images
            currentFrame += 1
        return img

    
    def take_photo(self, cap):
        for i in range(5):
            cap.grab()
            _, img = cap.read()
        return img
    
    
    def show_photo(self, img, text="Image"):
        # Display the image and wait for the user to press a key
        cv2.imshow(text, img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def stop_stream(self, cap):
        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()

    def close_window(self):
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    stream = Stream()
    cap = cv2.VideoCapture(0)
    img = stream.take_photo(cap)
    stream.stop_stream(cap)
    stream.show_photo(img)

