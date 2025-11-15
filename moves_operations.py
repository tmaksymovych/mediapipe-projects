import cv2
import mediapipe as mp
import time
import HandTrackingModule as htm
# from math import hypot
import pyautogui


pTime = 0
cTime = 0
cap = cv2.VideoCapture(1)
detector = htm.handDetector()
finger_was_up = False
click_count = 0
last_event_time = 0
DOUBLE_CLICK_WINDOW = 0.5

while True:
    success, img = cap.read()
    if not success:
        break
    img = cv2.flip(img,1)
    img = detector.findHands(img)
    leftH_pos = detector.findPositionByLabel(img, label="Right", draw=False)
    if len(leftH_pos) != 0:
        finger_tip = leftH_pos[8]
        finger_pip = leftH_pos[7]
        
        y_tip = finger_tip[2]
        y_dip = finger_pip[2]

        finger_is_up = (y_tip < y_dip)
        
        if finger_is_up == True and finger_was_up == False:
            click_count += 1

            if click_count == 2:
                time_diff = time.time() - last_event_time
                if time_diff < DOUBLE_CLICK_WINDOW:
                    pyautogui.press("up")
                    click_count = 0
                else:
                    click_count = 1
                    last_event_time = time.time()
            elif click_count == 1:
                last_event_time = time.time()
        if time.time() - last_event_time > DOUBLE_CLICK_WINDOW and click_count == 1:
            pyautogui.press("down")
            click_count = 0

        finger_was_up = finger_is_up

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,255),3)

    cv2.imshow("Image", img) 
    cv2.waitKey(1)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()