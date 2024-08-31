import cv2
import mediapipe as mp
import time
from math import pow
import pyautogui as pg

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands(min_detection_confidence=0.8)
mpDraw = mp.solutions.drawing_utils


def findHands(frames, draw=True):
    global results

    imgRGB = cv2.cvtColor(frames, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            if draw:
                mpDraw.draw_landmarks(frames, hand_landmarks, mpHands.HAND_CONNECTIONS)

    return frames


def findPositions(frames, results, handNo=0, draw=True):

    landmarkList = []

    # landmarkList = [[0, 200, 360], [1, 320, 460], [2, 200, 360], [3, 320, 460], [4, 200, 360], [5, 320, 460], [6, 200, 360], [7, 320, 460]]

    if results.multi_hand_landmarks:
        myHand = results.multi_hand_landmarks[handNo]
        for index, landmark in enumerate(myHand.landmark):
            height, width, channels = frames.shape
            cord_x, cord_y = int(landmark.x*width), int(landmark.y*height)
            # print(index, cord_x, cord_y)
            landmarkList.append([index, cord_x, cord_y])
            if draw:
                cv2.circle(frames, (cord_x, cord_y), 5,
                           (255, 0, 255), cv2.FILLED)

    return landmarkList

def distance(x1, x2, y1, y2):
    dist = pow(pow((x2-x1), 2) + pow((y2-y1), 2), 0.5)
    return dist

def main():
    previous_time = 0
    current_time = 0

    tip = [4, 8, 12, 16, 20]
    bottom = [3, 6, 10, 14, 18]

    while True:
        ret, frames = cap.read()

        frames = findHands(frames)
        landmarkList = findPositions(frames, results)
        if len(landmarkList) > 0:
            fingers = []
            print(distance(landmarkList[4][1],landmarkList[9][1],landmarkList[4][2], landmarkList[9][2]))
            if distance(landmarkList[4][1],landmarkList[9][1],landmarkList[4][2], landmarkList[9][2]) > 40:
                    fingers.append(1)
            else:
                fingers.append(0)
            for num in range(1, 5):
                if landmarkList[tip[num]][2] < landmarkList[bottom[num]][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            # print(fingers)
            gesture(fingers, landmarkList)

        current_time = time.time( )
        fps = int(1/(current_time-previous_time))
        previous_time = current_time

        cv2.putText(frames, f"FPS : {int(fps)}", (20, 50),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0))
 
        cv2.imshow("video", frames)
        k = cv2.waitKey(1)
        if k == ord("q"):
            break


def gesture(lst, landmarkList):
    # thumb, index, middle, ring, pinky
    gest_1 = [0, 1, 0, 0, 0]
    gest_2 = [0, 1, 1, 0, 0]
    gest_3 = [1, 0, 0, 0, 0]
    gest_4 = [1, 1, 1, 1, 1]
    gest_5 = [0, 1, 1, 1, 1]
    gest_6 = [0, 1, 0, 0, 0]
    
    if lst == gest_1:
        pg.press("up")
        # print("Volume Increased \n")
    elif lst == gest_2:
        pg.press("down")
        # print("Volume Decreased \n")
    elif lst == gest_3:
        if landmarkList[20][1] < landmarkList[4][1]:
            pg.press("left")
        elif landmarkList[20][1] > landmarkList[4][1]:
            pg.press("right")
        # print("Play, Pause\n")
    elif lst == gest_4:
        pg.press("space")
    elif lst == gest_5:
        pg.hotkey("win", "d ")
        # print("Play, Pause\n")
    elif lst == gest_6:
        pg.hotkey("alt", "f4 ")
    time.sleep(0.5)
    

if __name__=='__main__':
    main()
