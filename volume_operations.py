import cv2
import HandTrackingModule as htm
import time
from math import hypot
import numpy as np
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

pTime = 0
cap = cv2.VideoCapture(0)
detector = htm.handDetector()
devices = AudioUtilities.GetSpeakers()
volume = devices.EndpointVolume # type: ignore

SMOOTHING_FACTOR = 0.2
smoothed_scalar = 0.5

is_calibration = False
new_min = 999
new_max = 0


HAND_MIN_LENGTH = 10
HAND_MAX_LENGTH = 115
VOL_MIN_SCALAR = 0.02 # 0%
VOL_MAX_SCALAR = 0.99 # 100%

def volume_change_process (hand_position:list) ->bool:
    
    pinky_is_up = None
    ringf_is_down = None
    middlef_is_down = None

    if hand_position[20][2] < hand_position[19][2]:
        pinky_is_up = True
    else:
        pinky_is_up = False

    if hand_position[16][2] > hand_position[13][2]:
        ringf_is_down = True
    else:
        ringf_is_down = False

    if hand_position[12][2] > hand_position[9][2]:
        middlef_is_down = True
    else:
        middlef_is_down = False

    if pinky_is_up == True and ringf_is_down == True and middlef_is_down == True:
            return True
    else:
        return False

while True:
    success, img = cap.read()
    if not success:
        break
    img = cv2.flip(img,1)
    img = detector.findHands(img)
    leftH_pos = detector.findPositionByLabel(img, label="Left", draw=False)
    if len(leftH_pos) != 0:

        finger_tip = leftH_pos[8]
        thumb_tip = leftH_pos[4]

        cat_x = finger_tip[1] - thumb_tip[1]
        cat_y = finger_tip[2] - thumb_tip[2]

        length_between_fingers = hypot(cat_x, cat_y)

        if is_calibration:
            new_min = min(new_min, length_between_fingers)
            new_max = max(new_max, length_between_fingers)
            cv2.putText(img, 'CALIBRATING...', (100, 100), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)
        elif volume_change_process(leftH_pos):
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