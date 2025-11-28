import os
import json
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pickle
from collections import Counter

class GestureTrainer:
    def __init__(self, data_dir="data/gestures", model_dir="models"):
        self.data_dir = data_dir
        self.model_dir = model_dir
        os.makedirs(model_dir, exist_ok=True)
        
        self.gesture_map = {
            'moving': 0,
            'clicking': 1,
            'forward': 2,
            'backward': 3,
            'volume_up': 4,
            'volume_down': 5,
            'next_video': 6,
            'waiting': 7
        }
    
    def load_data(self):
        """Load tất cả dữ liệu từ các thư mục"""
        X = []
        y = []
        
        for gesture_name, label in self.gesture_map.items():
            gesture_dir = os.path.join(self.data_dir, gesture_name)
            
            if not os.path.exists(gesture_dir):
                print(f"Warning: {gesture_dir} not found, skipping...")
                continue
            
            json_files = [f for f in os.listdir(gesture_dir) if f.endswith('.json')]
            print(f"Loading {len(json_files)} samples for {gesture_name}...")
            
            for json_file in json_files:
                filepath = os.path.join(gesture_dir, json_file)
                try:
                    with open(filepath, 'r') as f:
                        data = json.load(f)
                    
                    features = np.array(data['features'])
                    X.append(features)
                    y.append(label)
                except Exception as e:
                    print(f"Error loading {filepath}: {e}")
        
        if len(X) == 0:
            return None, None
        
        X = np.array(X)
        y = np.array(y)
        
        print(f"\nTotal samples: {len(X)}")
        print(f"Feature shape: {X.shape}")
        print(f"Class distribution:")
        class_counts = Counter(y)
        for label, count in sorted(class_counts.items()):
            gesture_name = [k for k, v in self.gesture_map.items() if v == label][0]
            print(f"  {gesture_name} (label {label}): {count} samples")
        
        return X, y
    
    def train_single_model(self, X_train, X_test, y_train, y_test, model_type):
        """Train một model cụ thể"""
        # Chọn mô hình
        if model_type == 'random_forest':
            model = RandomForestClassifier(
                n_estimators=100, 
                random_state=42, 
                n_jobs=-1,
                max_depth=20,
                min_samples_split=5
            )
            model_name = "Random Forest"
        elif model_type == 'svm':
            model = SVC(kernel='rbf', probability=True, random_state=42, C=1.0, gamma='scale')
            model_name = "SVM"
        elif model_type == 'mlp':
            model = MLPClassifier(
                hidden_layer_sizes=(128, 64), 
                max_iter=500, 
                random_state=42,
                learning_rate='adaptive'
            )
            model_name = "MLP Neural Network"
        else:
            raise ValueError(f"Unknown model type: {model_type}")
        
        print(f"\n{'─'*70}")
        print(f" Training {model_name}...")
        print(f"{'─'*70}")
        
        # Train
        model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"✓ {model_name} trained successfully")
        print(f"  Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
        
        return model, accuracy, y_pred
    
    def train_and_compare(self):
        """Train tất cả models và chỉ lưu model tốt nhất"""
        X, y = self.load_data()
        
        if X is None or len(X) == 0:
            print("Error: No data found! Please collect data first using auto_collect_data.py")
            return None
        
        # Kiểm tra số lượng mẫu tối thiểu
        min_samples = 10
        class_counts = Counter(y)
        for label, count in class_counts.items():
            if count < min_samples:
                gesture_name = [k for k, v in self.gesture_map.items() if v == label][0]
                print(f"⚠ Warning: {gesture_name} has only {count} samples (recommended: at least {min_samples})")
        
        # Split data
        if len(np.unique(y)) > 1:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y
            )
        else:
            print("⚠ Warning: Only one class found, using simple split")
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
        
        print(f"\n✓ Training samples: {len(X_train)}")
        print(f"✓ Test samples: {len(X_test)}")
        
        print("\n" + "="*70)
        print("TRAINING ALL MODELS")
        print("="*70)
        
        # Train tất cả models
        models_results = {}
        model_types = ['random_forest', 'svm', 'mlp']
        model_names = {
            'random_forest': 'Random Forest',
            'svm': 'SVM',
            'mlp': 'MLP Neural Network'
        }
        
        for model_type in model_types:
            model, accuracy, y_pred = self.train_single_model(
                X_train, X_test, y_train, y_test, model_type
            )
            models_results[model_type] = {
                'model': model,
                'name': model_names[model_type],
                'accuracy': accuracy,
                'y_pred': y_pred
            }
        
        # So sánh models
        print("\n" + "="*70)
        print("MODEL COMPARISON")
        print("="*70 + "\n")
        
        print(f"{'Model':<25} {'Accuracy':<15} {'Status'}")
        print("─" * 70)
        
        for model_type, result in models_results.items():
            acc = result['accuracy']
            status = "" if acc < 0.9 else "✓ Good" if acc < 0.95 else "✓✓ Excellent"
            print(f"{result['name']:<25} {acc:.4f} ({acc*100:.2f}%)  {status}")
        
        # Tìm model tốt nhất
        best_model_type = max(models_results.items(), key=lambda x: x[1]['accuracy'])[0]
        best_result = models_results[best_model_type]
        best_model = best_result['model']
        best_accuracy = best_result['accuracy']
        best_name = best_result['name']
        
        print("\n" + "="*70)
        print(f"🏆 BEST MODEL: {best_name}")
        print(f"   Accuracy: {best_accuracy:.4f} ({best_accuracy*100:.2f}%)")
        print("="*70)
        
        # Hiển thị chi tiết model tốt nhất
        print(f"\n{'='*70}")
        print(f"DETAILED REPORT: {best_name}")
        print(f"{'='*70}\n")
        
        print("Classification Report:")
        # Lấy các classes thực tế có trong y_test
        unique_classes = np.unique(y_test)
        target_names = [name for name in sorted(self.gesture_map.keys(), key=lambda x: self.gesture_map[x]) 
                       if self.gesture_map[name] in unique_classes]
        print(classification_report(y_test, best_result['y_pred'], 
                                   labels=unique_classes,
                                   target_names=target_names,
                                   zero_division=0))
        
        # Confusion Matrix
        print("\nConfusion Matrix:")
        cm = confusion_matrix(y_test, best_result['y_pred'], labels=unique_classes)
        print("Predicted ->", end="")
        for i in range(len(target_names)):
            print(f"\t{target_names[i][:8]}", end="")
        print("\nActual")
        for i, row in enumerate(cm):
            print(f"{target_names[i][:8]}", end="")
            for val in row:
                print(f"\t{val}", end="")
            print()
        
        # Lưu CHỈ model tốt nhất
        print(f"\n{'='*70}")
        print("SAVING BEST MODEL")
        print(f"{'='*70}\n")
        
        model_path = os.path.join(self.model_dir, f"gesture_model_{best_model_type}.pkl")
        with open(model_path, 'wb') as f:
            pickle.dump(best_model, f)
        
        print(f"✓ Model saved to: {model_path}")
        
        # Save metadata - convert numpy types to Python native types
        class_dist = Counter(y)
        class_dist_dict = {str(k): int(v) for k, v in class_dist.items()}
        
        metadata = {
            'model_type': best_model_type,
            'model_name': best_name,
            'accuracy': float(best_accuracy),
            'n_samples': int(len(X)),
            'n_train_samples': int(len(X_train)),
            'n_test_samples': int(len(X_test)),
            'n_features': int(X.shape[1]),
            'n_classes': int(len(np.unique(y))),
            'gesture_map': {k: int(v) for k, v in self.gesture_map.items()},
            'class_distribution': class_dist_dict,
            'all_models_comparison': {
                result['name']: {
                    'accuracy': float(result['accuracy']),
                    'is_best': model_type == best_model_type
                } for model_type, result in models_results.items()
            }
        }
        
        metadata_path = os.path.join(self.model_dir, "model_metadata.json")
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"✓ Metadata saved to: {metadata_path}")
        
        print(f"\n{'='*70}")
        print(" TRAINING COMPLETE!")
        print(f"{'='*70}")
        print(f"\n Summary:")
        print(f"   • Best Model: {best_name}")
        print(f"   • Accuracy: {best_accuracy:.4f} ({best_accuracy*100:.2f}%)")
        print(f"   • Total Samples: {len(X)}")
        print(f"   • Features: {X.shape[1]}")
        print(f"   • Classes: {len(np.unique(y))}")
        print(f"\n Ready to use in VirtualMouse.py!")
        
        return best_model

def main():
    """Main entry point"""
    print("="*70)
    print("GESTURE RECOGNITION MODEL TRAINING")
    print("="*70)
    print("\nTraining all models and selecting the best one...\n")
    
    trainer = GestureTrainer()
    trainer.train_and_compare()

if __name__ == "__main__":
    main()
