import cv2 as cv

class Button:
    def __init__(self):
        self.step = 60
        self.wStep = 370
        self.hStep = 120
        self.buttonProps = []
        self.equation = ''

        self.buttonList = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            ["C", "0", "+", "="]
        ]

        for y in range(4):
            ypos = y*self.step + self.hStep
            for x in range(4):
                xpos = x*self.step + self.wStep
                self.buttonProps.append([xpos, ypos, xpos+self.step, ypos+self.step, self.buttonList[y][x]])

    def drawButtons(self, img):
        cv.rectangle(img, (self.wStep, self.hStep), (self.wStep + (self.step*4), self.step), (250, 255, 250), cv.FILLED)
        cv.rectangle(img, (self.wStep, self.hStep), (self.wStep + (self.step*4), self.step), (40, 40, 40), 2)

        for button in self.buttonProps:
            cv.rectangle(img, (button[0], button[1]), (button[2], button[3]), (250, 255, 250), cv.FILLED)
            cv.rectangle(img, (button[0], button[1]), (button[2], button[3]), (40, 40, 40), 2)
            cv.putText(img, button[4], (button[0] + 22, button[1] + 35), cv.FONT_HERSHEY_PLAIN, 1.4, (30, 30, 30), 1)

    def selectButton(self, img, xpos, ypos):
        for index, button in enumerate(self.buttonProps):
            if (xpos[0] > button[0] and button[2] > xpos[1]) and ypos[0] > button[1] and button[3] > ypos[1]:
                cv.rectangle(img, (button[0], button[1]), (button[2], button[3]), (250, 255, 250), cv.FILLED)
                cv.rectangle(img, (button[0], button[1]), (button[2], button[3]), (40, 40, 40), 3)
                cv.putText(img, button[4], (button[0] + 22, button[1] + 35), cv.FONT_HERSHEY_PLAIN, 1.4, (30, 30, 30), 2)

                if self.buttonList[int(index/4)][int(index%4)] == "=":
                    self.equation = str(self.evaluate())
                elif self.buttonList[int(index/4)][int(index%4)] == "C":
                    self.equation = self.equation[:-1]
                else:
                    self.equation += self.buttonList[int(index/4)][int(index%4)]

    def evaluate(self):
        return eval(self.equation)

    def getEquation(self):
        return self.equation