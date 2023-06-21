import cv2

# Capturing video from webcam:
cap = cv2.VideoCapture(0)

def takePIC():
    for i in range(5):
        cap.grab()
        _ , img  = cap.read()
    return img

currentFrame = 0
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Handles the mirroring of the current frame
    frame = cv2.flip(frame,1)

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame',gray)

    img = takePIC()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # To stop duplicate images
    currentFrame += 1



# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

# Display the image
cv2.imshow("Image", img)
 
# Wait for the user to press a key
cv2.waitKey(0)
 
# Close all windows
cv2.destroyAllWindows()

def returnImg():
    return img
