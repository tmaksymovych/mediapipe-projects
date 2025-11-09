import pyautogui


class GestureController:
    def __init__(self, swipe_threshold=100, action_cooldown=3.0):
        

        self.last_static_action_time = 0
        self.ACTION_COOLDOWN = action_cooldown

        self.swipe_mode = False
        self.swipe_start_X = 0
        self.last_swipe_time = 0
        self.SWIPE_COOLDOWN = action_cooldown
        self.SWIPE_THRESHOLD = swipe_threshold

    def update(self, cTime, fingers, lmList):
        """
        Главный "маршрутизатор". main.py вызывает ТОЛЬКО его.
        cTime: Текущее время (time.time())
        fingers: Список [0, 0, 0, 0, 0]
        lmList: Список координат (для свайпа)
        """
        if self.swipe_mode == True:
            self._handle_swipe_mode(cTime, fingers, lmList)
        else:
            self._handle_swipe_mode(cTime, fingers, lmList)
            self._handle_static_gestures(cTime, fingers)

    def _handle_static_gestures(self, cTime, fingers):
        """Обрабатывает "одноразовые" жесты: Кулак и Ладонь"""

        if (cTime - self.last_static_action_time) < self.ACTION_COOLDOWN:
            return
        
        if fingers == [0,0,0,0,0]:
            pyautogui.press("k")
            self.last_static_action_time = cTime

        elif fingers == [1,1,1,1,1]:
            pyautogui.press("f")
            self.last_static_action_time = cTime

    def _handle_swipe_mode(self, cTime, fingers, lmList):

        is_iba_chotko = (fingers == [1,0,0,0,1])

        if is_iba_chotko and not self.swipe_mode:
            self.swipe_mode = True
            self.swipe_start_X = lmList[0][1]
            self.last_swipe_time = cTime
            print("РЕЖИМ ПЕРЕМОТКИ: ВКЛ")

        elif is_iba_chotko and self.swipe_mode:
            cX = lmList[0][1]
            
            if (cTime - self.last_swipe_time) > self.SWIPE_COOLDOWN:

                if (cX - self.swipe_start_X) > self.SWIPE_THRESHOLD:
                    pyautogui.press("right")
                    print("СВАЙП: Вправо")
                    self.swipe_start_X = cX
                    self.last_swipe_time = cTime

                elif (self.swipe_start_X - cX) > self.SWIPE_THRESHOLD:
                    pyautogui.press("left")
                    print("СВАЙП: Влево")
                    self.swipe_start_X = cX
                    self.last_swipe_time = cTime
        elif not is_iba_chotko and self.swipe_mode:
            self.swipe_mode = False
            print("РЕЖИМ ПЕРЕМОТКИ: ВЫКЛ")