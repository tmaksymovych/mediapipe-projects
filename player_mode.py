import cv2
import mediapipe as mp
import time
import HandTrackingModule as htm



def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = htm.handDetector()
    while True:
        success, img = cap.read()
        if not success:
            break
        img = detector.findHands(img)
        leftH_pos = detector.findPositionByLabel(img, label="Left", draw=False)
        # if len(lmList) != 0:
        #     print(lmList[4])
        print(leftH_pos)

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255),3)

        cv2.imshow("Image", img) 
        cv2.waitKey(1)

if __name__ == "__main__":
    main()