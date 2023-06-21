import cv2

class Stream():
    def __init__(self):
        pass

    def start_stream(self):
        cap = cv2.VideoCapture(0)
        currentFrame = 0
        while(True):
            # Capture frame-by-frame
            _, frame = cap.read()
            
            # Display the video in gray scale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imshow('frame',gray)

            img = self.take_photo(cap)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.stop_stream(cap)
                break

            # To stop duplicate images
            currentFrame += 1
        return img


    def take_photo(self, cap):
        for i in range(5):
            cap.grab()
            _ , img  = cap.read()
        return img

    def show_photo(self, img):
        # Display the image and wait for the user to press a key
        cv2.imshow("Image", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def stop_stream(self, cap):
        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    stream = Stream()
    img = stream.start_stream()
    stream.show_photo(img)
    # stream.take_photo()
    # stream.stop_stream()