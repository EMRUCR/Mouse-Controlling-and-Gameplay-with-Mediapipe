# Hand Gesture Controller with MediaPipe 
(I had this part created in GPT. I was too lazy to write it down, to be honest :D)

This project uses MediaPipe, OpenCV, PyAutoGUI and PyDirectInput to control the mouse and basic game inputs with hand gestures.

## Files

```text
MouseWithHands.py
GameWithHands.py
```

## Requirements

Install the required libraries:

```bash
pip install mediapipe opencv-python pyautogui pydirectinput
```

Or create a `requirements.txt` file:

```txt
mediapipe
opencv-python
pyautogui
pydirectinput
```

Then install:

```bash
pip install -r requirements.txt
```

---

# MouseWithHands.py

`MouseWithHands.py` controls the desktop mouse using hand gestures.

## Mouse Controls

| Gesture | Action |
|---|---|
| Move wrist | Move mouse cursor |
| Thumb + Index finger | Hold left mouse button |
| Thumb + Middle finger | Single left click |
| Thumb + Ring finger | Single right click |

## Mouse Gesture Explanation

The wrist landmark is used for mouse movement.

```text
Wrist movement -> Mouse cursor movement
```

Finger tip distances are used for click detection.

```text
Thumb tip + Index tip  -> Left mouse hold
Thumb tip + Middle tip -> Left click
Thumb tip + Ring tip   -> Right click
```

If the distance between two fingertips is lower than `CLICK_DISTANCE`, the related mouse action is triggered.

Default value:

```python
CLICK_DISTANCE = 0.05
```

Lower `CLICK_DISTANCE` means the fingers must be closer to trigger an action.

Higher `CLICK_DISTANCE` makes gestures easier to trigger, but it can cause accidental clicks.

---

# GameWithHands.py

`GameWithHands.py` controls game inputs using both hands.

## Right Hand Controls

The right hand is used for camera movement, shooting, aiming, reload and weapon switching.

| Gesture | Action |
|---|---|
| Move right wrist | Move mouse / camera |
| Thumb + Index finger | Hold left click / Shoot |
| Thumb + Middle finger | Right click / Aim |
| Thumb + Ring finger | Press `1` / Change weapon |
| Thumb + Pinky finger | Press `R` / Reload |

## Left Hand Controls

The left hand is used for movement and action keys.

| Gesture | Action |
|---|---|
| Thumb + Index finger | Hold `W` / Walk forward |
| Thumb + Middle finger | Press `Shift` / Run |
| Thumb + Ring finger | Press `C` / Crouch |
| Thumb + Pinky finger | Press `E` / Melee / Interact |

---

## Full Gesture Mapping

### Right Hand

```text
Right wrist movement     -> Mouse / camera movement
Thumb + Index finger     -> Shoot
Thumb + Middle finger    -> Aim
Thumb + Ring finger      -> Change weapon
Thumb + Pinky finger     -> Reload
```

### Left Hand

```text
Thumb + Index finger     -> Walk forward
Thumb + Middle finger    -> Run
Thumb + Ring finger      -> Crouch
Thumb + Pinky finger     -> Melee / Interact
```

---

## Important Parameters

### Click Distance

```python
CLICK_DISTANCE = 0.04
```

Controls how close two fingers must be to trigger an action.

Lower value:

```text
Fewer accidental triggers, but gestures become harder.
```

Higher value:

```text
Gestures become easier, but false triggers may increase.
```

---

### Analog Speed

```python
ANALOG_SPEED = 150
```

Controls mouse or camera movement speed in `GameWithHands.py`.

Higher value means faster camera movement.

---

### Analog Smooth

```python
ANALOG_SMOOTH = 0.8
```

Controls movement smoothing.

Higher value:

```text
Faster response, less smoothing.
```

Lower value:

```text
Smoother movement, slower response.
```

---

### Analog Deadzone

```python
ANALOG_DEADZONE = 0.015
```

Prevents small unwanted hand movements from moving the camera.

Lower value makes the camera more sensitive.

Higher value makes small hand movements ignored.

---

## How to Run

For mouse control:

```bash
python MouseWithHands.py
```

For game control:

```bash
python GameWithHands.py
```

Press `Q` in the camera window to quit.

---

## Notes

- A webcam is required.
- Good lighting improves hand tracking accuracy.
- `MouseWithHands.py` uses PyAutoGUI for desktop mouse control.
- `GameWithHands.py` uses PyDirectInput for better game input compatibility.
- This project is a prototype for gesture-based mouse and game control.
