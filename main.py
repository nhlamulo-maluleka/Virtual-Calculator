import cv2 as cv
import mediapipe as mp
import numpy as np
import time
from HandModel import H_Model
from cvzone.HandTrackingModule import HandDetector

cap = cv.VideoCapture(0)

mpHands = mp.solutions.hands
handObject = mpHands.Hands(max_num_hands=1)
mpDraw = mp.solutions.drawing_utils

screenSize = cv.WINDOW_NORMAL
positions = []
cTime = 0
pTime = 0
color1 = (0, 255, 255)
color2 = (255, 255, 0)
detector = HandDetector(detectionCon=0.8)
delayCounter = 0

track = H_Model()

while True:
    success, frame = cap.read()
    cTime = time.time()
    frame = cv.flip(frame, flipCode=1)
    img = frame.copy()
    # img = np.zeros_like(img)
    frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    # hands, img = detector.findHands(img, flipType=False)

    # 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

    handResults = handObject.process(frame)

    track.drawButtons(img)
    track.detectHands(img, handResults)
    cv.putText(img, track.getEquation(), (track.wStep+10, track.hStep - int(track.step//2) + 10), cv.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 1)
    track.displayImage(img, screenSize)
    
    if cv.waitKey(1) & 0xFF == ord('q'):
        cv.destroyAllWindows()
        break
    elif cv.waitKey(1) & 0xFF == ord('f'):
        if screenSize == cv.WINDOW_NORMAL:
            screenSize = cv.WINDOW_FULLSCREEN
        elif screenSize == cv.WINDOW_FULLSCREEN:
            screenSize = cv.WINDOW_NORMAL
    
    fps = int(1//(cTime - pTime))
    pTime = cTime
    cv.putText(img, f"FPS: {str(fps)}", (10, 30), cv.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1)
