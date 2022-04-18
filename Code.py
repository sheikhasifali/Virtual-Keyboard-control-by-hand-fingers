import cv2
import cvzone
import numpy as np
from time import sleep
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Controller


cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8)

keys=[["Q","W","E","R","T","Y","U","I","O","p"],
      ["A","S","D","F","G","H","J","K","L",":"],
      ["Z","X","C","V","B","N","M",",",".","/"]]

finaltext=""

keyboard=Controller()

def drawAll(img,mylist):
    for button in mylist:
        x, y = button.pos
        h, w = button.size
        cv2.rectangle(img, button.pos, (x + w, y + h), (150, 0, 10), cv2.FILLED)
        cv2.putText(img, button.text, (x + 18, y + 60), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

    return img
  #with transperency
    """
def transparent_layout(img, mylist):
    imgNew = np.zeros_like(img, np.uint8)
    for button in mylist:
        x, y = button.pos
        cvzone.cornerRect(imgNew, (button.pos[0], button.pos[1],
                                                   button.size[0],button.size[0]), 20 ,rt=0)
        cv2.rectangle(imgNew, button.pos, (x + button.size[0], y + button.size[1]),
                                   (255, 144, 30), cv2.FILLED)
        cv2.putText(imgNew, button.text, (x + 20, y + 65),
                    cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 4)

    out = img.copy()
    alpaha = 0.5
    mask = imgNew.astype(bool)
    print(mask.shape)
    out[mask] = cv2.addWeighted(img, alpaha, imgNew, 1-alpaha, 0)[mask]
    return out
"""
class Button():
    def __init__(self,pos,text,size=[80,80]):
        self.pos=pos
        self.size=size
        self.text=text






mylist=[]
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        mylist.append(Button([100 * j + 50, 100 * i + 50], key))


while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList,bboxInfo=detector.findPosition(img)

    img=drawAll(img,mylist)

    if lmList:
        for button in mylist:
            x,y=button.pos
            w,h=button.size

            if x< lmList[8][0]<x+w and y<lmList[8][1]<y+h:
                cv2.rectangle(img, button.pos, (x + w, y + h), (255, 144, 30), cv2.FILLED)
                cv2.putText(img, button.text, (x + 18, y + 60), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

                l, _, _ = detector.findDistance(8, 12, img)
                print(l)

                if l < 50:
                    keyboard.press(button.text)
                    cv2.rectangle(img, button.pos, (x + w, y + h), (0, 200, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 18, y + 60), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

                    finaltext += button.text
                    sleep(0.35)

    cv2.rectangle(img, (50,350), (700, 450), (10, 20, 30), cv2.FILLED)
    cv2.putText(img, finaltext, (60, 425), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

    cv2.imshow("Virtual keyboard",img)
    cv2.waitKey(1)
cap.release()
cv2.destryAllWindows()
