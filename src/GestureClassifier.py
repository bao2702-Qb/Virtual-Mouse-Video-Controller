import pickle
import json
import os
import numpy as np
import HandTrackingModule as htm

class GestureClassifier:
    def __init__(self, model_path="models/gesture_model_random_forest.pkl"):
        self.model_path = model_path
        self.detector = htm.handDetector(maxHands=1)
        self.model = None
        self.metadata = None
        self.gesture_map = {}
        
        # Load model
        if os.path.exists(model_path):
            try:
                with open(model_path, 'rb') as f:
                    self.model = pickle.load(f)
                print(f"✓ Model loaded from {model_path}")
            except Exception as e:
                print(f"Error loading model: {e}")
                self.model = None
        else:
            print(f"Warning: Model not found at {model_path}")
            print("Please train the model first using train_model.py")
            self.model = None
        
        # Load metadata
        metadata_path = os.path.join(os.path.dirname(model_path), "model_metadata.json")
        if os.path.exists(metadata_path):
            try:
                with open(metadata_path, 'r') as f:
                    self.metadata = json.load(f)
                self.gesture_map = {v: k for k, v in self.metadata['gesture_map'].items()}
                print(f"✓ Metadata loaded: {self.metadata['n_samples']} samples, "
                      f"accuracy: {self.metadata['accuracy']:.2%}")
            except Exception as e:
                print(f"Error loading metadata: {e}")
                # Default mapping
                self.gesture_map = {
                    0: 'moving', 1: 'clicking', 2: 'forward', 3: 'backward',
                    4: 'volume_up', 5: 'volume_down', 6: 'next_video', 7: 'waiting'
                }
        else:
            # Default mapping
            self.gesture_map = {
                0: 'moving', 1: 'clicking', 2: 'forward', 3: 'backward',
                4: 'volume_up', 5: 'volume_down', 6: 'next_video', 7: 'waiting'
            }
    
    def is_available(self):
        """Kiểm tra xem model có sẵn không"""
        return self.model is not None
    
    def extract_landmarks(self, lmList):
        """Trích xuất landmarks giống như khi collect data"""
        if len(lmList) == 0:
            return None
        
        wrist = np.array([lmList[0][1], lmList[0][2]])
        features = []
        
        # Normalize landmarks relative to wrist
        for lm in lmList:
            rel_x = (lm[1] - wrist[0]) / 640.0
            rel_y = (lm[2] - wrist[1]) / 480.0
            features.extend([rel_x, rel_y])
        
        # Thêm thông tin về distances từ wrist đến fingertips
        if len(lmList) >= 21:
            for tip_id in [4, 8, 12, 16, 20]:  # Thumb, Index, Middle, Ring, Pinky
                tip = np.array([lmList[tip_id][1], lmList[tip_id][2]])
                dist = np.linalg.norm(tip - wrist) / 640.0
                features.append(dist)
        
        return np.array(features)
    
    def predict(self, lmList):
        """Dự đoán cử chỉ từ landmarks"""
        if not self.is_available():
            return 'waiting', 0.0
        
        if len(lmList) == 0:
            return 'waiting', 0.0
        
        try:
            features = self.extract_landmarks(lmList)
            
            # Kiểm tra số features
            if self.metadata and features.shape[0] != self.metadata['n_features']:
                print(f"Warning: Feature mismatch. Expected {self.metadata['n_features']}, got {features.shape[0]}")
                return 'waiting', 0.0
            
            features = features.reshape(1, -1)
            
            # Predict
            prediction = self.model.predict(features)[0]
            probability = self.model.predict_proba(features)[0]
            confidence = max(probability)
            
            gesture = self.gesture_map.get(prediction, 'waiting')
            
            return gesture, confidence
        except Exception as e:
            print(f"Error in prediction: {e}")
            return 'waiting', 0.0

