import cv2
import time
import sys
import keyboard
from HandTrackingModule import HandDetector




def most_frequent(List: list) -> int:
    return max(set(List), key=List.count)


def analyze_fingers(sample: int, player) -> list:
    cap = cv2.VideoCapture(0)
    pTime = 0
    cTime = 0
    instance = HandDetector(maxHands=1)
    tipIds = [4, 8, 12, 16, 20]
    frequency = []
    item = ""
    while True:
        success, img = cap.read()
        img = instance.find_hands(img, draw=True)
        lmList = instance.find_position(img)
        if len(lmList) is not 0:
            fingers = []
            # Thumb
            if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
            # 4 fingers
            for id in range(1, 5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            totalFingers = fingers.count(1)
            frequency.append(totalFingers)
            if len(frequency) > sample:
                frequency = []
        if len(frequency) == sample:
            item = translate(most_frequent(frequency))
        cv2.putText(img, item, (10, 100), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        cv2.putText(img, f"player {str(player)}:", (10, 65), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        cv2.imshow("Image", img)
        cv2.waitKey(1)
        if keyboard.is_pressed("space"):
            return item

def translate(number):
    if number == 2 or number == 3:
        return "schaar"
    elif number == 5 or number == 4:
        return "papier"
    elif number is 0 or number is 1:
        return "steen"

def logic(player1, player2):
    if player1 is player2:
        return "Equal"

    if player1 == "schaar" and player2 == "papier":
        return "player 1"
    if player1 == "papier" and player2 == "schaar":
        return "player 2"

    if player1 == "papier" and player2 == "steen":
        return "player 2"
    if player1 == "steen" and player2 == "papier":
        return "player 1"

    if player1 == "steen" and player2 == "schaar":
        return "player 1"
    if player1 == "schaar" and player2 == "steen":
        return "player 2"


def main():
    player1 = analyze_fingers(10, player=1)
    player2 = analyze_fingers(10, player=2)
    result = (logic(player1, player2) + " WINS !!")
    cap = cv2.VideoCapture(0)
    instance = HandDetector(maxHands=1)
    while True:
        success, img = cap.read()
        img = instance.find_hands(img, draw=True)
        cv2.putText(img, result, (10, 100), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        cv2.imshow("Image", img)
        cv2.waitKey(1)
        if keyboard.is_pressed("space"):
            break


if __name__ == "__main__":
    main()
