import cv2
import time
from HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
pTime = 0
cTime = 0
instance = HandDetector()
tipIds = [4, 8, 12, 16, 20]


def most_frequent(List: list) -> int:
    return max(set(List), key=List.count)


def analyze_fingers(sample: int) -> list:
    frequency = []
    while len(frequency) < sample:
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
        # cTime = time.time()
        # fps = 1 / (cTime - pTime)
        # pTime = cTime
        # cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        cv2.imshow("Image", img)
        cv2.waitKey(1)
    return frequency


def translate(number):
    if number == 2 or number == 3:
        return "ciseaux"
    elif number == 5 or number == 4:
        return "feuille"
    elif number is 0 or number is 1:
        return "pierre"


def do():
    frequency = analyze_fingers(10)
    number = most_frequent(frequency)
    result = translate(number)
    return result


def main():
    print("player 1: ")
    print(do())
    print("player 2 in 3 seconds...")
    time.sleep(3)
    print("player 2: ")
    print(do())


if __name__ == "__main__":
    main()
