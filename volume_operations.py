import cv2
import HandTrackingModule as htm
import time
from math import hypot
import numpy as np
from pycaw.pycaw import AudioUtilities

pTime = 0
cap = cv2.VideoCapture(0)
detector = htm.handDetector()
devices = AudioUtilities.GetSpeakers()
volume = devices.EndpointVolume

SMOOTHING_FACTOR = 0.2
smoothed_scalar = 0.5

is_calibration = False
new_min = 999
new_max = 0


HAND_MIN_LENGTH = 10
HAND_MAX_LENGTH = 115
VOL_MIN_SCALAR = 0.02 # 0%
VOL_MAX_SCALAR = 0.99 # 100%


while True:
    success, img = cap.read()
    if not success:
        break
    img = cv2.flip(img,1)
    img = detector.findHands(img)
    lmList = detector.findPositionByLabel(img, label="Left", draw=False)
    if len(lmList) != 0:
            
        finger_tip = lmList[8]
        thumb_tip = lmList[4]

        cat_x = finger_tip[1] - thumb_tip[1]
        cat_y = finger_tip[2] - thumb_tip[2]

        length_between_fingers = hypot(cat_x, cat_y)

        if is_calibration:
            new_min = min(new_min, length_between_fingers)
            new_max = max(new_max, length_between_fingers)
            cv2.putText(img, 'CALIBRATING...', (100, 100), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)
        else:


            vol_scalar = np.interp(length_between_fingers, 
                                [HAND_MIN_LENGTH, HAND_MAX_LENGTH], 
                                [VOL_MIN_SCALAR, VOL_MAX_SCALAR])

            smoothed_scalar = (SMOOTHING_FACTOR * vol_scalar) + ((1 - SMOOTHING_FACTOR) * smoothed_scalar)
            volume.SetMasterVolumeLevelScalar(smoothed_scalar, None)

            

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,255),3)

    cv2.imshow("Image", img)
    # ВЫЗЫВАЕМ ОДИН РАЗ
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break
    if key == ord('c'):
        is_calibration = not is_calibration
        if is_calibration:
            print("Режим калибровки. растяни и стени максимально пальци, чтобы настроить max/min значение громкости")
            new_min = 999
            new_max = 0
        else:
            HAND_MAX_LENGTH = new_max
            HAND_MIN_LENGTH = new_min
            print("Калибровка завершена!")


cap.release()
cv2.destroyAllWindows()