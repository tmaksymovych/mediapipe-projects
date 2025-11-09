import cv2
import time
import HandTrackingModule as htm
import GestureController as gs



def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = htm.handDetector()
    mode = gs.GestureController()
    

    while True:

        success, img = cap.read()
        img = cv2.flip(img,1)
        img = detector.findHands(img)
        lmList = detector.findPositionByLabel(img, label="Right", draw=False)

        if len(lmList) != 0:
            
            fingers = []
            curTime = time.time()
            tipIds = [4, 8, 12, 16, 20]
            
            if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:     # from thumb
                fingers.append(1)
            else:
                fingers.append(0)
                
            for id in range(1, 5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:   #for remained fingers
                    fingers.append(1)
                else:
                    fingers.append(0)
                
            print(fingers)

            mode.update(cTime=curTime, fingers=fingers, lmList=lmList)
        else:
            if mode.swipe_mode == True:
                mode.swipe_mode = False
                    
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255),3)

        cv2.imshow("Image", img) 
        cv2.waitKey(1)



if __name__ == "__main__":
    main()