import numpy as np
import cv2 as cv
import mediapipe as mp
from ButtonModel import Button

class H_Model(Button):
    def __init__(self):
        super().__init__()
        self.windowName = "Virtual Paint"
        self.mpHands = mp.solutions.hands
        self.handObject = self.mpHands.Hands(max_num_hands=1)
        self.mpDraw = mp.solutions.drawing_utils
        self.delayCounter = 0

    def displayImage(self, img, size):
        cv.namedWindow(self.windowName, cv.WINDOW_NORMAL)
        cv.setWindowProperty(self.windowName, cv.WINDOW_NORMAL, size)
        cv.imshow(self.windowName, img)

    def calculateDistance(self, xpos, ypos):
        return int(np.sqrt((xpos[0] - xpos[1])**2 + (ypos[0] - ypos[1])**2))

    def detectHands(self, img, handResults):
        cx1, cy1, cx2, cy2 = None, None, None, None

        if handResults.multi_hand_landmarks:
            resultObject = handResults.multi_hand_landmarks

            if resultObject:
                for hand in resultObject:
                    self.mpDraw.draw_landmarks(img, hand, self.mpHands.HAND_CONNECTIONS)
                    for id, lm in enumerate(hand.landmark):
                        h,w,c = img.shape
                        
                        if id == 8:
                            cx1, cy1 = int(lm.x*w), int(lm.y*h)
                            cv.circle(img, (cx1, cy1), 7, (255, 255, 0), cv.FILLED)

                        if id == 12:
                            cx2, cy2 = int(lm.x*w), int(lm.y*h)
                            cv.circle(img, (cx2, cy2), 7, (0, 255, 255), cv.FILLED)

                        if cx1 and cy1 and cx2 and cy2 and self.delayCounter == 0:
                            cv.line(img, (cx1, cy1), (cx2, cy2), (32, 78, 123), 3)
                            if self.calculateDistance((cx1, cx2), (cy1, cy2)) < 35:
                                self.selectButton(img, (cx1, cx2), (cy1, cy2))
                                self.delayCounter = 1

        if self.delayCounter > 0:
            self.delayCounter += 1
            if self.delayCounter > 10:
                self.delayCounter = 0
