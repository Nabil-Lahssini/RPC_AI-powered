import cv2
import keyboard
from HandTrackingModule import HandDetector
from collections import deque


def most_frequent(List: list) -> int:
    """Returns the most frequent value from the last X frames"""
    return max(set(List), key=List.count)


def analyze_fingers(sample: int, player) -> list:
    cap = cv2.VideoCapture(0)
    pTime = 0
    cTime = 0
    instance = HandDetector(maxHands=2)
    tipIds = [4, 8, 12, 16, 20, 24, 28, 32, 36, 40]
    frequency = deque(maxlen=sample)
    frequency2 = deque(maxlen=sample)
    item = ""
    item2 = ""
    while True:
        success, img = cap.read()
        img = instance.find_hands(img, draw=True)
        lmList = instance.find_position(img)
        if len(lmList) is not 0:
            fingers = []
            fingers2 = []
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
            if len(lmList) > 40:
                # Thumb
                if lmList[tipIds[6]][1] < lmList[tipIds[6] - 1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
                for id in range(6, 10):
                    if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                        fingers2.append(1)
                    else:
                        fingers2.append(0)
                totalFingers2 = fingers2.count(1)
                frequency2.append(totalFingers2)
            totalFingers = fingers.count(1)
            frequency.append(totalFingers)
        if len(frequency) == sample:
            item = translate(most_frequent(frequency))
        if len(frequency2) == sample:
            item2 = translate(most_frequent(frequency2))
        cv2.putText(img, item, (10, 100), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        cv2.putText(img, item2, (10, 65), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        cv2.imshow("Image", img)
        cv2.waitKey(1)
        if keyboard.is_pressed("space"):
            return item, item2


def translate(number: int) -> str:
    """Detects if its 'schaar' 'steen' or 'papier'"""
    if number == 2 or number == 3:
        return "schaar"
    elif number == 5 or number == 4:
        return "papier"
    elif number is 0 or number is 1:
        return "steen"


def logic(player1: str, player2: str) -> str:
    """By the lack of 'switch case' in older versions of Python I used an ugly if if if case..."""
    if player1 is player2:
        return "Nobody"
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
    player1, player2 = analyze_fingers(10, player=1)
    result = (logic(player1, player2) + " WINS !!")
    cap = cv2.VideoCapture(0)
    instance = HandDetector(maxHands=3)
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
