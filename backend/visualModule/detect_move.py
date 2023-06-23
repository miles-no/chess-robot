import cv2

def detect_move():
    preState = cv2.imread('testImages/PreState.jpg')
    currState = cv2.imread('testImages/CurrState.jpg')
    cv2.imshow('preState', preState)
    cv2.imshow('currState', currState)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



if __name__ == "__main__":
    detect_move()