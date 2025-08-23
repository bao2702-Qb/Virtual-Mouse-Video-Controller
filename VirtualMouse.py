import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy
import keyboard   # for sending video control keys

##########################
wCam, hCam = 640, 480
frameR = 100 # Frame Reduction
smoothening = 8
#########################

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

# Click state management to prevent multiple clicks
last_click_time = 0
click_cooldown = 0.3 # 0.3 seconds between clicks
click_triggered = False

# Gesture cooldown
last_gesture_time = 0
gesture_cooldown = 1  # 1 second between video actions

cap = cv2.VideoCapture(0)
# # Create persistent window
# cv2.namedWindow("Virtual Mouse + Video Control", cv2.WINDOW_NORMAL)
# cv2.setWindowProperty("Virtual Mouse + Video Control", cv2.WND_PROP_TOPMOST, 1)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands=1)
wScr, hScr = autopy.screen.size()

# Helper function for video controls
def  trigger_action(action):
    global last_gesture_time
    if time.time() - last_gesture_time > gesture_cooldown:
        if action == "forward":
            keyboard.press_and_release('right')
            print("Forward 10s triggered")
        elif action == "backward":
            keyboard.press_and_release('left')
            print("Backward 10s triggered")
        last_gesture_time = time.time()

while True:
    # 1. Find hand Landmarks
    success, img = cap.read()
    img = cv2.flip(img, 1)  # Flip frame horizontally (mirror effect)
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)
    
    current_time = time.time()
    
    # 2. Get the tip of the index and middle fingers
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]  # Index finger tip
        x2, y2 = lmList[12][1:] # Middle finger tip
    
        # 3. Check which fingers are up
        fingers,thumb_direction = detector.fingersUp()
        
        # Draw interaction frame
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
        (255, 0, 255), 2)
        
        # ---------------- Cursor Control ---------------- #
        # 4. Only Index Finger : Moving Mode
        if fingers[1] == 1 and fingers[2] == 0:
            # 5. Convert Coordinates
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
            # 6. Smoothen Values
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening
        
            # 7. Move Mouse
            autopy.mouse.move(clocX, clocY)
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY
            
            click_triggered = False
            cv2.putText(img, "MOVING", (50, 120), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.8, (255, 0, 255), 2)
            
        # 8. Both Index and middle fingers are up : Clicking Mode
        elif fingers[1] == 1 and fingers[2] == 1:
            # 9. Find distance between fingers
            length, img, lineInfo = detector.findDistance(8, 12, img)
            
            if length < 30:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                cv2.putText(img, "CLICK READY", (50, 120), cv2.FONT_HERSHEY_SIMPLEX, 
                           0.8, (0, 255, 0), 2)
                
                if not click_triggered and (current_time - last_click_time > click_cooldown):
                    autopy.mouse.click()
                    last_click_time = current_time
                    click_triggered = True
                    print(f"Click performed! Distance: {length:.1f}")
            else:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 165, 255), cv2.FILLED)
                cv2.putText(img, f"Distance: {int(length)}", (50, 120), cv2.FONT_HERSHEY_SIMPLEX, 
                           0.6, (0, 165, 255), 2)
                cv2.putText(img, "Bring fingers closer", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 
                           0.5, (255, 255, 255), 1)
                if length > 40:
                    click_triggered = False
        
        # ---------------- Video Control ---------------- #

        # 10. Thumb gestures (forward/backward)
        elif fingers == [1,0,0,0,0]:
            if thumb_direction == "left":
                trigger_action("backward")
                cv2.putText(img, "BACKWARD", (50,120),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,165,255), 2)
            elif thumb_direction == "right":
                trigger_action("forward")
                cv2.putText(img, "FORWARD", (50,120),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

        else:
            cv2.putText(img, "WAITING", (50, 120), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.8, (128, 128, 128), 2)
            click_triggered = False   
    
    # 11. Frame Rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f"FPS: {int(fps)}", (20, 50), cv2.FONT_HERSHEY_PLAIN, 2,
    (255, 0, 0), 2)
    
    # Instructions
    cv2.putText(img, "Index finger: Move cursor", (10, hCam - 80), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.putText(img, "Index + Middle close: Click", (10, hCam - 60), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.putText(img, "Index + Middle close: Play/Pause", (10, hCam - 40), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    cv2.putText(img, "Thumb left/right Direction: Back/Forward", (10, hCam - 20), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
    
    # 12. Display
    cv2.imshow("Virtual Mouse + Video Control", img)
    key = cv2.waitKey(1) & 0xFF
    if key == 27:   # ESC to quit
        break

cap.release()
cv2.destroyAllWindows()
