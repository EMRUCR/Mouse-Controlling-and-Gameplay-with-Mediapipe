import mediapipe as mp
import math as m
import cv2
import pyautogui
import time


# Necessary Func
def distance(p1, p2):
    return m.dist(p1, p2)

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands = 1,
    model_complexity=0,
    min_detection_confidence = 0.5,
    min_tracking_confidence = 0.5)

# for screen and mouse clicking
screen_w, screen_h = pyautogui.size()
pyautogui.PAUSE = 0
last_mouse_time = 0
MOUSE_INTERVAL = 1 / 165
SENSITIVITY = 3
smooth_x = screen_w // 2
smooth_y = screen_h // 2
SMOOTH = 0.2
left_is_clicking = False
left_hold_is_clicking = False
right_is_clicking = False

CLICK_DISTANCE = 0.05


# for capturing
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:

            # Hand Landmarks
            lm = hand_landmarks.landmark
            WRIST = lm[0]
            THUMB = [lm[1], lm[2], lm[3], lm[4]]
            INDEX = [lm[5], lm[6], lm[7], lm[8]]
            MIDDLE = [lm[9], lm[10], lm[11], lm[12]]
            RING = [lm[13], lm[14], lm[15], lm[16]]

            x = WRIST.x
            y = WRIST.y
            
            mouse_x = int((x - 0.5) * screen_w * SENSITIVITY + screen_w / 2)
            mouse_y = int((y - 0.5) * screen_h * SENSITIVITY + screen_h / 2)
            
            mouse_x = max(0, min(screen_w - 1, mouse_x))
            mouse_y = max(0, min(screen_h - 1, mouse_y))

            smooth_x = smooth_x + (mouse_x - smooth_x) * SMOOTH
            smooth_y = smooth_y + (mouse_y - smooth_y) * SMOOTH            


            now = time.time()
            if now - last_mouse_time > MOUSE_INTERVAL:
                pyautogui.moveTo(int(smooth_x), int(smooth_y))
                last_mouse_time = now

            THUMB_TIP = (lm[4].x, lm[4].y)
            INDEX_TIP = (lm[8].x, lm[8].y)
            MIDDLE_TIP = (lm[12].x,lm[12].y)
            RING_TIP = (lm[16].x,lm[16].y)  


            # FOR LEFT MOUSE CLICK HOLD
            left_click_distance = distance(THUMB_TIP, INDEX_TIP)

            if left_click_distance < CLICK_DISTANCE and not left_is_clicking:
                pyautogui.mouseDown(button="left")
                left_is_clicking = True
            
            elif left_click_distance >= CLICK_DISTANCE and left_is_clicking:
                pyautogui.mouseUp(button="left")
                left_is_clicking = False


            # FOR LEFT MOUSE CLICK
            left_holdclick_distance = distance(THUMB_TIP, MIDDLE_TIP)

            if left_holdclick_distance < CLICK_DISTANCE and not left_hold_is_clicking:
                pyautogui.click(button="left")
                left_hold_is_clicking = True
            
            elif left_holdclick_distance >= CLICK_DISTANCE and left_hold_is_clicking:
                left_hold_is_clicking = False

            # FOR RIGHT MOUSE CLICK
            right_click_distance = distance(THUMB_TIP,RING_TIP)

            if right_click_distance < CLICK_DISTANCE and not right_is_clicking:
                pyautogui.click(button="right")
                right_is_clicking = True
            
            elif right_click_distance >= CLICK_DISTANCE:
                right_is_clicking = False

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )
        
    cv2.imshow("Cam",frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
hands.close()
cv2.destroyAllWindows()