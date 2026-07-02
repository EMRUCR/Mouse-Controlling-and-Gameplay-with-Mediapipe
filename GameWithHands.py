import mediapipe as mp
import math as m
import cv2
import pydirectinput

def distance(p1, p2):
    return m.dist(p1, p2)


mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands = 2,
    model_complexity=0,
    min_detection_confidence = 0.5,
    min_tracking_confidence = 0.5)


pydirectinput.PAUSE = 0

# For Gamepad analog
ANALOG_CENTER_X = 0.7
ANALOG_CENTER_Y = 0.7

ANALOG_DEADZONE = 0.015
ANALOG_SPEED = 150
ANALOG_SMOOTH = 0.8
CLICK_DISTANCE = 0.04

analog_move_x = 0
analog_move_y = 0

def analog_axis(value):
    if abs(value) < ANALOG_DEADZONE:
        return 0

    sign = 1 if value > 0 else -1

    normalized = (abs(value) - ANALOG_DEADZONE) / (0.5 - ANALOG_DEADZONE)
    normalized = max(0, min(1, normalized))

    return sign * (normalized ** 1.5)

# One-time key states
r_is_pressed = False
c_is_pressed = False
e_is_pressed = False
w_is_pressed = False
shift_is_pressed = False
one_is_pressed = False

# Mouse states
left_is_clicking = False
right_is_clicking = False

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks and results.multi_handedness:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):

            hand_label = handedness.classification[0].label

            # HAND LANDMARKS
            lm = hand_landmarks.landmark
            WRIST = lm[0]
            THUMB = [lm[1], lm[2], lm[3], lm[4]]
            INDEX = [lm[5], lm[6], lm[7], lm[8]]
            MIDDLE = [lm[9], lm[10], lm[11], lm[12]]
            RING = [lm[13], lm[14], lm[15], lm[16]]
            PINKY = [lm[17], lm[18], lm[19], lm[20]]

            THUMB_TIP = (lm[4].x, lm[4].y)
            INDEX_TIP = (lm[8].x, lm[8].y)
            MIDDLE_TIP = (lm[12].x,lm[12].y)
            RING_TIP = (lm[16].x,lm[16].y) 
            PINKY_TIP = (lm[20].x,lm[20].y) 


            if hand_label == "Right":


                x = WRIST.x
                y = WRIST.y
                
                raw_x = x - ANALOG_CENTER_X
                raw_y = y - ANALOG_CENTER_Y
                
                axis_x = analog_axis(raw_x)
                axis_y = analog_axis(raw_y)
                
                target_move_x = axis_x * ANALOG_SPEED
                target_move_y = axis_y * ANALOG_SPEED

                analog_move_x = analog_move_x + (target_move_x - analog_move_x) * ANALOG_SMOOTH
                analog_move_y = analog_move_y + (target_move_y - analog_move_y) * ANALOG_SMOOTH

                final_move_x = int(analog_move_x)
                final_move_y = int(analog_move_y)

                if abs(final_move_x) < 2:
                    final_move_x = 0

                if abs(final_move_y) < 2:
                    final_move_y = 0

                if final_move_x != 0 or final_move_y != 0:
                    pydirectinput.moveRel(final_move_x, final_move_y, duration=0)

                # FOR LEFT MOUSE HOLD TO SHOOTING
                left_click_distance = distance(THUMB_TIP, INDEX_TIP)

                if left_click_distance < CLICK_DISTANCE and not left_is_clicking:
                    pydirectinput.mouseDown(button="left")
                    left_is_clicking = True

                elif left_click_distance >= CLICK_DISTANCE and left_is_clicking:
                    pydirectinput.mouseUp(button="left")
                    left_is_clicking = False

                # FOR RIGHT MOUSE CLICK TO TAKE SIGHT
                right_click_distance = distance(THUMB_TIP, MIDDLE_TIP)
                if right_click_distance < CLICK_DISTANCE and not right_is_clicking:
                    pydirectinput.click(button="right")
                    right_is_clicking = True
                elif right_click_distance >= CLICK_DISTANCE and right_is_clicking:
                    right_is_clicking = False

                # PRESS 1 TO CHANGE GUN
                one_key_distance = distance(THUMB_TIP, RING_TIP)
                
                if one_key_distance < CLICK_DISTANCE and not one_is_pressed:
                    pydirectinput.press("1")
                    one_is_pressed = True
                
                elif one_key_distance >= CLICK_DISTANCE and one_is_pressed:
                    one_is_pressed = False
                
                # PRESS THE R FOR RELOADING
                r_key_distance = distance(THUMB_TIP, PINKY_TIP)
                
                if r_key_distance < CLICK_DISTANCE and not r_is_pressed:
                    pydirectinput.press("r")
                    r_is_pressed = True
                
                elif r_key_distance >= CLICK_DISTANCE and r_is_pressed:
                    r_is_pressed = False



            elif hand_label == "Left":


                # W FOR WALK
                w_key_dist = distance(THUMB_TIP, INDEX_TIP)

                if w_key_dist < CLICK_DISTANCE and not w_is_pressed:
                    pydirectinput.keyDown("w")
                    w_is_pressed = True
                
                elif w_key_dist >= CLICK_DISTANCE and w_is_pressed:
                    pydirectinput.keyUp("w")
                    w_is_pressed = False
                
                # SHIFT FOR RUN
                shift_key_distance = distance(THUMB_TIP, MIDDLE_TIP)
                
                if shift_key_distance < CLICK_DISTANCE and not shift_is_pressed:
                    pydirectinput.press("shift")
                    shift_is_pressed = True
                
                elif shift_key_distance >= CLICK_DISTANCE and shift_is_pressed:
                    shift_is_pressed = False
                
                # C FOR CROUCH
                c_key_distance = distance(THUMB_TIP, RING_TIP)
                
                if c_key_distance < CLICK_DISTANCE and not c_is_pressed:
                    pydirectinput.press("c")
                    c_is_pressed = True
                
                elif c_key_distance >= CLICK_DISTANCE and c_is_pressed:
                    c_is_pressed = False
                    
                # E FOR MELEE
                e_key_distance = distance(THUMB_TIP, PINKY_TIP)
                
                if e_key_distance < CLICK_DISTANCE and not e_is_pressed:
                    pydirectinput.press("e")
                    e_is_pressed = True
                
                elif e_key_distance >= CLICK_DISTANCE and e_is_pressed:
                    e_is_pressed = False

                
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