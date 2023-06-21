#Code heavily inspired from https://github.com/EDGE-tronics/Chess-Robot/
import cv2
import numpy as np
import string
import time
import os


#Import for camera to use for calibration

#Test images of chessboards
cbPattern = cv2.imread('chessBoardImages/chess-board.png')
simulatedBoard = cv2.imread('chessBoardImages/bettercb.png')
blackandwhitecb = cv2.imread('chessBoardImages/blackandwhitecb.png')
screenshot = cv2.imread('chessBoardImages/screenshot.png')
greenframe = cv2.imread('chessBoardImages/greenframe.png')
obstacle = cv2.imread('chessBoardImages/obstacle.png')
bildechess = cv2.imread('chessBoardImages/bildechess.png')
croppedchess = cv2.imread('chessBoardImages/chess-cropped.png')
mainProj = cv2.imread('chessBoardImages/mainProj.png')
rotatedCBPattern = cv2.imread('chessBoardImages/rotatedcbpattern.png')
CBPatternGray = cv2.imread('chessBoardImages/CBPatternGray.png')
closeUpMainProj = cv2.imread('chessBoardImages/closeUpMainProj.png')

#cbPattern is essentially an input of a default chessboard image
#img is captured frame from camera
def findTransformation(img,cbPattern):

    patternSize = (7,7)
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # retCB - Boolean. Returns true if the chessboard pattern corners are detected, false otherwise.
    # cornersCB - Returns corners in matrix representing coordinates of the chessboard pattern corners.
    # Find chessboard corners
    retCB, cornersCB = cv2.findChessboardCorners(cbPattern, patternSize, cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)
    retIMG, cornersIMG = cv2.findChessboardCorners(imgGray, patternSize, cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)

    if retIMG == 0:
        H = 0
    else:
        H, _ = cv2.findHomography(cornersIMG, cornersCB)     # Find the transformation matrix
    
    return(retIMG, H)

#Applies necessary rotation to actual board to properly determine play
def applyRotation(img,R):
    if R.any() != 0:
        #img.shape[1::-1] retrieves the width of the image and reverses it. 
        img = cv2.warpAffine(img, R, img.shape[1::-1], flags=cv2.INTER_LINEAR)
        
    return(img)

#Applies homography matrix for calibration
def applyHomography(img,H):

    imgNEW = cv2.warpPerspective(img, H, (400, 400))
    
    return(imgNEW)

#Draws quadrants to assist users in calibration(Essentially helps the program to determine which quadrant
# white is located)
def drawQuadrants(img):

    # Draw quadrants and numbers on image
    imgquad = img.copy()
    cv2.line(imgquad, (200, 0), (200, 400), (0,255,0), 3)
    cv2.line(imgquad, (0, 200), (400, 200), (0,255,0), 3)
    imgquad = cv2.putText(imgquad, '1', (80, 120) , cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 3, cv2.LINE_AA)
    imgquad = cv2.putText(imgquad, '2', (280, 120) , cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 3, cv2.LINE_AA) 
    imgquad = cv2.putText(imgquad, '3', (280, 320) , cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 3, cv2.LINE_AA) 
    imgquad = cv2.putText(imgquad, '4', (80, 320) , cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 3, cv2.LINE_AA) 

    return(imgquad)

#Finds the rotation matrix to properly rotate the chessboard pattern
def findRotation(theta):

    if theta != 0:
        rotMAT = cv2.getRotationMatrix2D(tuple(np.array((400,400)[1::-1])/2), theta, 1.0)
    else:
        rotMAT = np.zeros((2,2))

    return(rotMAT)

#Detects a player's move by comparing previous frame to current frame
#by selecting regions that have undergone the most significant changes in color
def findMoves(img1, img2):

    size = 50
    img1SQ = img2SQ = []
    largest = [0, 0, 0, 0]
    coordinates = [0, 0, 0, 0]
    for y in range(0,8*size,size):
        for x in range(0,8*size,size):
            img1SQ = img1[x:x+size, y:y+size]
            img2SQ = img2[x:x+size, y:y+size]
            dist = cv2.norm(img2SQ, img1SQ)
            for z in range(0,4):
                if dist >= largest[z]:
                    largest.insert(z,dist)
                    # Save in algebraic chess notation
                    coordinates.insert(z,(string.ascii_lowercase[int(x/size)]+str(int(y/size+1))))
                    largest.pop()
                    coordinates.pop()
                    break

    # Make threshold with a percentage of the change in color of the biggest two
    thresh = (largest[0]+largest[1])/2*(0.5)
    for t in range(3,1,-1):
        if largest[t] < thresh:
            coordinates.pop()
    
    return(coordinates)

#Used for testing chessboard pattern recognition using OpenCV's function findChessboardCorners()
def patternRecognizer(img):
    
    patternSize = (7,7)
    makeGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    retCB, cornersCB = cv2.findChessboardCorners(makeGray, patternSize, cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)
    imagePreviewName = "Original image"
    if retCB:
        print("Pattern found...")
        # Refine the corners to subpixel accuracy (Might be used for higher accuracy, but not necessarily needed)
        # criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        # cv2.cornerSubPix(makeGray, cornersCB, (11, 11), (-1, -1), criteria)
        # Draw the corners on the image
        cv2.drawChessboardCorners(img, patternSize, cornersCB, retCB)
            # Display the image
        cv2.imshow(imagePreviewName, img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return True
    else: 
        print("No pattern found")
        return False
    

if __name__ == "__main__":
    patternRecognizer(cbPattern)    

 
