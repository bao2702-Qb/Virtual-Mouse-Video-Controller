import cv2
import numpy as np
import HandTrackingModule as htm
import time
import pyautogui
import keyboard   # for sending video control keys
import os
import json

# Try to import GestureClassifier for ML-based gesture recognition
try:
    from GestureClassifier import GestureClassifier
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    print("GestureClassifier not available, using rule-based detection only")

# Auto-select mode based on comparison
def load_auto_mode():
    config_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "model_config.json")
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            mode = config.get('selected_mode', 'rule-based')
            ml_acc = config.get('ml_accuracy', 0)
            rule_acc = config.get('rule_accuracy', 0)
            print(f"\n{'='*50}")
            print(f"AUTO-SELECTED MODE: {mode.upper()}")
            print(f"  ML accuracy: {ml_acc*100:.2f}%")
            print(f"  Rule-based: {rule_acc*100:.2f}%")
            print(f"{'='*50}\n")
            return mode == "ml"
        except Exception as e:
            print(f"Could not load config: {e}")
    return True  # Default to ML if no config

USE_ML_MODEL = load_auto_mode()

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

# Volume cooldown
last_volume_time = 0
volume_cooldown = 0.3  # 0.3 seconds between volume actions

# Next video cooldown
last_next_video_time = 0
next_video_cooldown = 1  # 1 second between next video actions

cap = cv2.VideoCapture(0)
# # Create persistent window
# cv2.namedWindow("Virtual Mouse + Video Control", cv2.WINDOW_NORMAL)
# cv2.setWindowProperty("Virtual Mouse + Video Control", cv2.WND_PROP_TOPMOST, 1)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands=1)
wScr, hScr = pyautogui.size()

# Initialize ML model if available
ml_classifier = None
if USE_ML_MODEL:
    # Auto-detect any ML model in models directory
    model_dir = "models"
    model_path = None
    
    if os.path.exists(model_dir):
        model_files = [f for f in os.listdir(model_dir) if f.startswith('gesture_model_') and f.endswith('.pkl')]
        if model_files:
            model_path = os.path.join(model_dir, model_files[0])
    
    if model_path and os.path.exists(model_path):
        try:
            ml_classifier = GestureClassifier(model_path)
            if ml_classifier.is_available():
                model_name = os.path.basename(model_path).replace('gesture_model_', '').replace('.pkl', '').replace('_', ' ').title()
                print(f"✓ ML Model loaded successfully! ({model_name})")
            else:
                print("⚠ ML Model file exists but failed to load, using rule-based")
                ml_classifier = None
        except Exception as e:
            print(f"⚠ Error loading ML model: {e}, using rule-based")
            ml_classifier = None
    else:
        print("ℹ ML Model not found, using rule-based detection")
        print("  To use ML model: Run auto_collect_data.py and train_model.py first")
else:
    print("ℹ Using rule-based detection only")

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

# Helper function for volume controls
def trigger_volume(direction):
    global last_volume_time
    if time.time() - last_volume_time > volume_cooldown:
        if direction == "up":
            pyautogui.press('volumeup')
            print("Volume UP triggered")
        elif direction == "down":
            pyautogui.press('volumedown')
            print("Volume DOWN triggered")
        last_volume_time = time.time()

# Helper function for next video
def trigger_next_video():
    global last_next_video_time
    if time.time() - last_next_video_time > next_video_cooldown:
        # Try multiple shortcuts for better compatibility
        keyboard.press_and_release('shift+n')  # YouTube next video
        print("Next video triggered (Shift+N)")
        last_next_video_time = time.time()

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
        
        # Get hand center for volume detection
        hand_center_y = bbox[1] + (bbox[3] - bbox[1]) // 2 if bbox else 0
    
        # 3. Check which fingers are up
        # Đảm bảo lmList đã được set trong detector trước khi gọi fingersUp()
        try:
            if len(lmList) > 0:
                fingers,thumb_direction = detector.fingersUp()
            else:
                fingers = [0, 0, 0, 0, 0]
                thumb_direction = "neutral"
        except (IndexError, AttributeError) as e:
            # Nếu có lỗi, set default values
            print(f"Error in fingersUp(): {e}")
            fingers = [0, 0, 0, 0, 0]
            thumb_direction = "neutral"
        
        # Try ML prediction first if available
        ml_gesture = None
        ml_confidence = 0.0
        if ml_classifier and ml_classifier.is_available():
            ml_gesture, ml_confidence = ml_classifier.predict(lmList)
        
        # Debug: Show current finger state
        fingers_str = f"Fingers: {fingers}"
        cv2.putText(img, fingers_str, (10, hCam - 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
        
        # Debug: Show thumb direction
        thumb_str = f"Thumb: {thumb_direction}"
        cv2.putText(img, thumb_str, (10, hCam - 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
        
        # Debug: Show gesture detection status với chi tiết
        if len(lmList) != 0:
            # Hiển thị chi tiết từng điều kiện
            debug_info = []
            debug_info.append(f"I:{fingers[1]} M:{fingers[2]} T:{fingers[0]}")
            
            # Kiểm tra từng điều kiện
            if fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
                debug_info.append("MOVING")
                cv2.putText(img, "DETECT: MOVING", (10, hCam - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            elif fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:
                debug_info.append("CLICKING")
                cv2.putText(img, "DETECT: CLICKING", (10, hCam - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            elif fingers[1] == 1 and fingers[0] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
                debug_info.append("VOLUME")
                cv2.putText(img, "DETECT: VOLUME", (10, hCam - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            elif fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0 and fingers[0] != 1:
                # Có thể là volume nhưng thumb chưa được detect
                debug_info.append("VOLUME? (thumb not detected)")
                cv2.putText(img, "VOLUME? (thumb not up)", (10, hCam - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 165, 0), 1)
            elif fingers == [1,0,0,0,0]:
                debug_info.append("FORWARD/BACKWARD")
                cv2.putText(img, "DETECT: THUMB", (10, hCam - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 200, 0), 2)
            else:
                debug_info.append("WAITING")
                # Hiển thị lý do không match
                reason = []
                if fingers[1] != 1:
                    reason.append("Index not up")
                if fingers[2] != 0 and fingers[1] == 1:
                    reason.append(f"Middle={fingers[2]}")
                if fingers[3] != 0:
                    reason.append(f"Ring={fingers[3]}")
                if fingers[4] != 0:
                    reason.append(f"Pinky={fingers[4]}")
                if fingers[0] == 1 and fingers[1] == 1:
                    reason.append("Thumb up")
                elif fingers[0] != 1 and fingers[1] == 1 and fingers[2] == 0:
                    reason.append("Thumb not up (for volume)")
                reason_str = " | ".join(reason) if reason else "No match"
                cv2.putText(img, f"WAITING: {reason_str}", (10, hCam - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.4, (128, 128, 128), 1)
            
            # In ra console để debug
            if len(debug_info) > 1:
                print(f"Debug: {debug_info[0]} -> {debug_info[1]}")
        
        # Show ML prediction if available
        if ml_gesture and ml_confidence > 0.5:
            ml_text = f"ML: {ml_gesture} ({ml_confidence:.2f})"
            cv2.putText(img, ml_text, (10, hCam - 15), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)
        
        # Draw interaction frame
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
        (255, 0, 255), 2)
        
        # Draw interaction frame
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
        (255, 0, 255), 2)
        
        # ---------------- Cursor Control ---------------- #
        # Use ML prediction if available and confident, otherwise use rule-based
        use_ml = ml_gesture and ml_confidence > 0.7
        
        # ---------------- Volume Control (KIỂM TRA TRƯỚC để tránh nhầm với moving) ---------------- #
        # Volume Control: Thumb GIƠ NGANG TRÁI (direction="left") + TẤT CẢ các ngón còn lại giơ lên
        # Điều kiện MẠNH HƠN moving để tránh nhầm lẫn
        if (use_ml and ml_gesture in ['volume_up', 'volume_down']) or \
           (not use_ml and fingers[0] == 1 and thumb_direction == "left" and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1):  # Thumb LEFT + tất cả ngón giơ lên
            
            # Tính khoảng cách giữa thumb và index
            thumb_index_distance = 0
            if len(lmList) >= 9:
                thumb_x, thumb_y = lmList[4][1:]  # Thumb tip
                index_x, index_y = lmList[8][1:]  # Index tip
                thumb_index_distance = np.hypot(index_x - thumb_x, index_y - thumb_y)
            
            VOLUME_UP_THRESHOLD = 120   # Dang rộng (khoảng cách lớn)
            VOLUME_DOWN_THRESHOLD = 70  # Chụm gần (khoảng cách nhỏ)
            
            # Vẽ line và circle để hiển thị khoảng cách
            if len(lmList) >= 9:
                thumb_x, thumb_y = lmList[4][1:]
                index_x, index_y = lmList[8][1:]
                cv2.line(img, (thumb_x, thumb_y), (index_x, index_y), (255, 0, 255), 3)
                cv2.circle(img, (thumb_x, thumb_y), 15, (255, 0, 255), cv2.FILLED)
                cv2.circle(img, (index_x, index_y), 15, (255, 0, 255), cv2.FILLED)
                cx, cy = (thumb_x + index_x) // 2, (thumb_y + index_y) // 2
                cv2.circle(img, (cx, cy), 10, (0, 0, 255), cv2.FILLED)
                cv2.putText(img, f"{int(thumb_index_distance)}px", (cx - 20, cy - 20),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            if use_ml:
                if ml_gesture == 'volume_up':
                    trigger_volume("up")
                    cv2.putText(img, "VOLUME UP", (50, 120),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
                elif ml_gesture == 'volume_down':
                    trigger_volume("down")
                    cv2.putText(img, "VOLUME DOWN", (50, 120),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)
            else:
                # Rule-based: Volume Up - dang rộng
                if thumb_index_distance > VOLUME_UP_THRESHOLD:
                    trigger_volume("up")
                    cv2.putText(img, "VOLUME UP", (50, 120),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
                    cv2.putText(img, f"Distance: {int(thumb_index_distance)}px", (50, 150),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
                # Rule-based: Volume Down - chụm gần
                elif thumb_index_distance < VOLUME_DOWN_THRESHOLD:
                    trigger_volume("down")
                    cv2.putText(img, "VOLUME DOWN", (50, 120),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)
                    cv2.putText(img, f"Distance: {int(thumb_index_distance)}px", (50, 150),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
                else:
                    cv2.putText(img, "VOLUME MODE", (50, 120),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,200,0), 2)
                    cv2.putText(img, f"Distance: {int(thumb_index_distance)}px", (50, 150),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
                    cv2.putText(img, f"Spread >{VOLUME_UP_THRESHOLD}px or Close <{VOLUME_DOWN_THRESHOLD}px", (50, 180),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255), 1)
        
        # 4. Only Index Finger : Moving Mode
        # Index up, middle/ring/pinky cụp (thumb tự do - KHÔNG kiểm tra)
        elif (use_ml and ml_gesture == 'moving') or \
           (not use_ml and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0):  # Index up, middle/ring/pinky cụp (thumb tự do)
            # 5. Convert Coordinates
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
            # 6. Smoothen Values
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening
        
            # 7. Move Mouse
            pyautogui.moveTo(clocX, clocY)
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY
            
            click_triggered = False
            cv2.putText(img, "MOVING", (50, 120), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.8, (255, 0, 255), 2)
            
        # 8. Both Index and middle fingers are up : Clicking Mode
        # Index và middle up, ring/pinky cụp (thumb tự do - KHÔNG kiểm tra)
        elif (use_ml and ml_gesture == 'clicking') or \
             (not use_ml and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0):  # Index và Middle up, ring/pinky cụp (thumb tự do)
            # 9. Find distance between fingers
            length, img, lineInfo = detector.findDistance(8, 12, img)
            
            if length < 30:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                cv2.putText(img, "CLICK READY", (50, 120), cv2.FONT_HERSHEY_SIMPLEX, 
                           0.8, (0, 255, 0), 2)
                
                if not click_triggered and (current_time - last_click_time > click_cooldown):
                    pyautogui.click()
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
        elif (use_ml and ml_gesture in ['forward', 'backward']) or (not use_ml and fingers == [1,0,0,0,0]):
            # Use ML prediction if available
            if use_ml:
                if ml_gesture == 'forward':
                    trigger_action("forward")
                    cv2.putText(img, "FORWARD", (50,120),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
                elif ml_gesture == 'backward':
                    trigger_action("backward")
                    cv2.putText(img, "BACKWARD", (50,120),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,165,255), 2)
            # Rule-based fallback
            else:
                if thumb_direction == "left":
                    trigger_action("backward")
                    cv2.putText(img, "BACKWARD", (50,120),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,165,255), 2)
                elif thumb_direction == "right":
                    trigger_action("forward")
                    cv2.putText(img, "FORWARD", (50,120),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

        # 12. All fingers up (except thumb) : Next Video
        # Chỉ kiểm tra 4 ngón: index, middle, ring, pinky đều giơ lên (thumb tự do)
        elif (use_ml and ml_gesture == 'next_video') or \
             (not use_ml and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1 and not (fingers[0] == 1 and thumb_direction == "left")):
            trigger_next_video()
            cv2.putText(img, "NEXT VIDEO", (50,120),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,255), 2)
            cv2.putText(img, "Shift+N Triggered!", (50, 150),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,255), 2)

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
    cv2.putText(img, "ONLY Index: Move cursor", (10, hCam - 120), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
    cv2.putText(img, "Index+Middle close: Click", (10, hCam - 105), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
    cv2.putText(img, "ONLY Thumb left/right: Back/Forward", (10, hCam - 90), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)
    cv2.putText(img, "Thumb LEFT + All fingers spread >120px: Vol Up", (10, hCam - 75), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 200, 0), 1)
    cv2.putText(img, "Thumb LEFT + All fingers close <70px: Vol Down", (10, hCam - 60), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 200, 0), 1)
    cv2.putText(img, "4 Fingers Up (no thumb LEFT): Next Video", (10, hCam - 45), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 255), 1)
    
    # Show detection mode
    mode_text = "ML Model" if (ml_classifier and ml_classifier.is_available()) else "Rule-Based"
    cv2.putText(img, f"Mode: {mode_text}", (wCam - 150, 30), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
    
    # 12. Display
    cv2.imshow("Virtual Mouse + Video Control", img)
    key = cv2.waitKey(1) & 0xFF
    if key == 27:   # ESC to quit
        break

cap.release()
cv2.destroyAllWindows()

def main():
    """Main entry point - runs the main loop"""
    pass  # Main loop runs at module level

if __name__ == "__main__":
    main()
