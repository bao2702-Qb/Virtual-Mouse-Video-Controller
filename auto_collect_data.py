import cv2
import numpy as np
import HandTrackingModule as htm
import json
import os
from datetime import datetime
import time

class AutoDataCollector:
    def __init__(self, data_dir="data/gestures", auto_save_interval=0.5):
        self.data_dir = data_dir
        self.auto_save_interval = auto_save_interval  # Lưu mỗi 0.5 giây
        self.detector = htm.handDetector(maxHands=1)
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 640)
        self.cap.set(4, 480)
        
        # Tạo thư mục
        self.gestures = {
            'moving': 0,
            'clicking': 1,
            'forward': 2,
            'backward': 3,
            'volume_up': 4,
            'volume_down': 5,
            'next_video': 6,
            'waiting': 7
        }
        
        for gesture in self.gestures.keys():
            os.makedirs(os.path.join(data_dir, gesture), exist_ok=True)
        
        self.last_save_time = {}
        self.counts = {gesture: 0 for gesture in self.gestures.keys()}
    
    def detect_gesture(self, lmList, bbox, fingers, thumb_direction):
        """Đã cập nhật logic để khớp với VirtualMouse.py"""
        if len(lmList) == 0:
            return 'waiting'
        
        # Tính khoảng cách giữa thumb và index cho volume control
        thumb_x, thumb_y = lmList[4][1:]  # Thumb tip
        index_x, index_y = lmList[8][1:]  # Index tip
        thumb_index_distance = np.hypot(index_x - thumb_x, index_y - thumb_y)
        
        # PRIORITY 1: Volume Control - Thumb LEFT + TẤT CẢ ngón giơ lên
        # Kiểm tra TRƯỚC để tránh nhầm với các cử chỉ khác
        if fingers[0] == 1 and thumb_direction == "left" and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
            # Volume Up: dang rộng (khoảng cách lớn)
            if thumb_index_distance > 120:
                return 'volume_up'
            # Volume Down: chụm gần (khoảng cách nhỏ)
            elif thumb_index_distance < 70:
                return 'volume_down'
            else:
                return 'waiting'  # Đang ở volume mode nhưng chưa dang/chụm đủ (70-120px)
        
        # PRIORITY 2: Moving - CHỈ ngon tro (thumb tự do, KHÔNG phải thumb left + all fingers)
        elif fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
            return 'moving'
        
        # PRIORITY 3: Clicking - ngon tro + ngon giua (thumb tự do)
        elif fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:
            x1, y1 = lmList[8][1:]
            x2, y2 = lmList[12][1:]
            length = np.hypot(x2 - x1, y2 - y1)
            if length < 30:
                return 'clicking'
            else:
                return 'waiting'  # Fingers up but not close enough
        
        # PRIORITY 4: Forward/Backward - chỉ thumb
        elif fingers == [1,0,0,0,0]:
            if thumb_direction == "left":
                return 'backward'
            elif thumb_direction == "right":
                return 'forward'
        
        # PRIORITY 5: Next Video - 4 ngón giơ lên (index, middle, ring, pinky), thumb tự do NHƯƠNG KHÔNG left
        elif fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1 and not (fingers[0] == 1 and thumb_direction == "left"):
            return 'next_video'
        
        return 'waiting'
    
    def extract_landmarks(self, lmList):
        """Trích xuất features từ landmarks - normalize relative to wrist"""
        if len(lmList) == 0:
            return None
        
        wrist = np.array([lmList[0][1], lmList[0][2]])
        features = []
        
        # Normalize landmarks relative to wrist
        for lm in lmList:
            rel_x = (lm[1] - wrist[0]) / 640.0
            rel_y = (lm[2] - wrist[1]) / 480.0
            features.extend([rel_x, rel_y])
        
        # Thêm thông tin về fingers state
        # Tính toán angles và distances giữa các điểm quan trọng
        if len(lmList) >= 21:
            # Distance từ wrist đến các fingertips
            for tip_id in [4, 8, 12, 16, 20]:  # Thumb, Index, Middle, Ring, Pinky
                tip = np.array([lmList[tip_id][1], lmList[tip_id][2]])
                dist = np.linalg.norm(tip - wrist) / 640.0  # Normalize
                features.append(dist)
        
        return np.array(features)
    
    def collect(self, duration_minutes=10):
        """Tự động collect trong khoảng thời gian"""
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        
        print("=== AUTO DATA COLLECTION MODE ===")
        print(f"Collecting for {duration_minutes} minutes...")
        print("Just make gestures naturally!")
        print("Gestures to collect:")
        for gesture, label in self.gestures.items():
            print(f"  {label}: {gesture}")
        print("\nPress 'q' to stop early")
        
        while time.time() < end_time:
            success, img = self.cap.read()
            if not success:
                continue
                
            img = cv2.flip(img, 1)
            img = self.detector.findHands(img)
            lmList, bbox = self.detector.findPosition(img, draw=False)
            
            current_time = time.time()
            elapsed = int(current_time - start_time)
            remaining = int(end_time - current_time)
            
            if len(lmList) != 0:
                fingers, thumb_direction = self.detector.fingersUp()
                gesture = self.detect_gesture(lmList, bbox, fingers, thumb_direction)
                
                # Vẽ visual feedback cho volume control
                if gesture in ['volume_up', 'volume_down'] and len(lmList) >= 9:
                    thumb_x, thumb_y = lmList[4][1:]
                    index_x, index_y = lmList[8][1:]
                    thumb_index_distance = np.hypot(index_x - thumb_x, index_y - thumb_y)
                    
                    # Vẽ đường nối thumb và index
                    cv2.line(img, (thumb_x, thumb_y), (index_x, index_y), (255, 0, 255), 3)
                    cv2.circle(img, (thumb_x, thumb_y), 15, (255, 0, 255), cv2.FILLED)
                    cv2.circle(img, (index_x, index_y), 15, (255, 0, 255), cv2.FILLED)
                    cx, cy = (thumb_x + index_x) // 2, (thumb_y + index_y) // 2
                    cv2.circle(img, (cx, cy), 10, (0, 0, 255), cv2.FILLED)
                    
                    # Hiển thị khoảng cách
                    cv2.putText(img, f"{int(thumb_index_distance)}px", (cx - 30, cy - 20),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                    cv2.putText(img, f">120=UP | <70=DOWN", (cx - 50, cy + 30),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 0), 1)
                
                # Visual feedback cho next_video
                if gesture == 'next_video':
                    cv2.rectangle(img, (bbox[0]-20, bbox[1]-20), (bbox[2]+20, bbox[3]+20),
                                 (255, 0, 255), 3)
                    cv2.putText(img, "4 Fingers UP!", (bbox[0], bbox[1]-30),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)
                
                # Auto save với interval
                if gesture != 'waiting':
                    last_save = self.last_save_time.get(gesture, 0)
                    if current_time - last_save >= self.auto_save_interval:
                        features = self.extract_landmarks(lmList)
                        
                        if features is not None:
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                            filepath = os.path.join(self.data_dir, gesture, f"{timestamp}.json")
                            
                            data = {
                                'features': features.tolist(),
                                'landmarks': lmList,
                                'gesture': gesture,
                                'label': self.gestures[gesture],
                                'fingers': fingers,
                                'thumb_direction': thumb_direction
                            }
                            
                            with open(filepath, 'w') as f:
                                json.dump(data, f)
                            
                            self.counts[gesture] += 1
                            self.last_save_time[gesture] = current_time
                
                # Hiển thị
                cv2.putText(img, f"Detected: {gesture}", (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(img, f"Fingers: {fingers} | Thumb: {thumb_direction}", (10, 55), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
                cv2.putText(img, f"Time: {elapsed}s / Remaining: {remaining}s", (10, 75), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            else:
                cv2.putText(img, "No hand detected", (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            # Hiển thị counts
            y_offset = 100
            for gesture, count in sorted(self.counts.items()):
                cv2.putText(img, f"{gesture}: {count}", (10, y_offset), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 0), 1)
                y_offset += 20
            
            cv2.imshow("Auto Data Collection", img)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == 27:
                break
        
        self.cap.release()
        cv2.destroyAllWindows()
        
        print("\n=== Collection Complete ===")
        total = sum(self.counts.values())
        for gesture, count in sorted(self.counts.items()):
            print(f"{gesture}: {count} samples")
        print(f"Total: {total} samples")
        
        return self.counts

if __name__ == "__main__":
    import sys
    
    duration = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    
    collector = AutoDataCollector()
    collector.collect(duration_minutes=duration)

