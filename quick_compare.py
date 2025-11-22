import os
import json
import numpy as np
import pickle
from sklearn.metrics import accuracy_score

def quick_compare():
    """So sánh nhanh ML model vs Rule-based"""
    
    print("\n" + "="*70)
    print("QUICK MODEL COMPARISON")
    print("="*70 + "\n")
    
    # Load ML model
    model_dir = "models"
    
    if not os.path.exists(model_dir):
        print(" Models directory not found!")
        print("   Run: python train_model.py first\n")
        return
    
    model_files = [f for f in os.listdir(model_dir) if f.endswith('.pkl') and 'gesture_model' in f]
    
    if len(model_files) == 0:
        print(" No trained model found!")
        print("   Run: python train_model.py first\n")
        return
    
    model_path = os.path.join(model_dir, model_files[0])
    
    print(f" Loading model: {model_files[0]}")
    
    try:
        with open(model_path, 'rb') as f:
            model_data = pickle.load(f)
        
        # Check if model_data is a dict (with metadata) or direct model object
        if isinstance(model_data, dict):
            ml_model = model_data.get('model', model_data)
            ml_name = model_data.get('model_name', 'Unknown')
            train_acc = model_data.get('accuracy', 0)
        else:
            # Direct model object
            ml_model = model_data
            ml_name = "ML Model"
            train_acc = 0
        
        # Try to load metadata from separate JSON file
        metadata_path = os.path.join(model_dir, "model_metadata.json")
        if os.path.exists(metadata_path) and train_acc == 0:
            try:
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)
                ml_name = metadata.get('model_name', ml_name)
                train_acc = metadata.get('accuracy', train_acc)
            except:
                pass  # Ignore JSON errors, use defaults
                
    except Exception as e:
        print(f" Error loading model: {e}\n")
        return
    
    # Load test data
    data_dir = "data/gestures"
    gesture_map = {
        'moving': 0, 
        'clicking': 1, 
        'forward': 2, 
        'backward': 3,
        'volume_up': 4, 
        'volume_down': 5, 
        'next_video': 6, 
        'waiting': 7
    }
    
    X, y = [], []
    gesture_counts = {}
    
    print(f" Loading test data from: {data_dir}")
    
    for gesture_name, label in gesture_map.items():
        gesture_dir = os.path.join(data_dir, gesture_name)
        if not os.path.exists(gesture_dir):
            continue
        
        files = [f for f in os.listdir(gesture_dir) if f.endswith('.json')]
        
        if len(files) == 0:
            continue
            
        gesture_counts[gesture_name] = len(files)
        
        for file in files:
            try:
                filepath = os.path.join(gesture_dir, file)
                with open(filepath, 'r') as f:
                    data = json.load(f)
                landmarks = np.array(data['features'])
                X.append(landmarks)
                y.append(label)
            except Exception as e:
                pass
    
    if len(X) == 0:
        print(" No test data found!")
        print("   Run: python auto_collect_data.py first\n")
        return
    
    X = np.array(X)
    y = np.array(y)
    
    print(f"✓ Loaded {len(X)} samples")
    print(f"  Gestures with data: {', '.join(gesture_counts.keys())}\n")
    
    # Test ML model
    print(" Testing ML model...")
    y_pred = ml_model.predict(X)
    ml_accuracy = accuracy_score(y, y_pred)
    
    # Calculate per-gesture accuracy
    unique_labels = np.unique(y)
    gesture_accuracies = {}
    
    for label in unique_labels:
        mask = (y == label)
        if mask.sum() > 0:
            acc = accuracy_score(y[mask], y_pred[mask])
            gesture_name = [k for k, v in gesture_map.items() if v == label][0]
            gesture_accuracies[gesture_name] = acc
    
    # Ước lượng rule-based (dựa trên kinh nghiệm)
    # Rule-based thường đạt 70-85% với gestures đơn giản
    rule_based_estimate = 0.78
    
    print("\n" + "="*70)
    print("COMPARISON RESULTS")
    print("="*70)
    
    print(f"\n{'Approach':<30} {'Accuracy':<20} {'Status'}")
    print("-"*70)
    print(f"{'ML Model (' + ml_name + ')':<30} {ml_accuracy:.4f} ({ml_accuracy*100:5.2f}%)")
    print(f"{'Rule-Based Logic (estimated)':<30} ~{rule_based_estimate:.4f} (~{rule_based_estimate*100:5.2f}%)")
    print("-"*70)
    
    if ml_accuracy > rule_based_estimate:
        diff = ml_accuracy - rule_based_estimate
        improvement = (diff / rule_based_estimate) * 100
        print(f"\n ML Model is BETTER!")
        print(f"   Improvement: +{diff:.4f} (+{improvement:.1f}%)")
        print(f"\n RECOMMENDATION: Use ML Model for better accuracy")
    elif ml_accuracy >= rule_based_estimate - 0.05:
        print(f"\n ML Model is COMPARABLE to Rule-Based")
        print(f"\n RECOMMENDATION: Use ML Model for better generalization")
    else:
        print(f"\n Rule-Based might be better")
        print(f"\n RECOMMENDATION: Collect more training data or tune ML model")
    
    print("\n" + "="*70)
    print("PER-GESTURE ML ACCURACY")
    print("="*70)
    
    for gesture_name in sorted(gesture_accuracies.keys(), key=lambda x: gesture_map[x]):
        acc = gesture_accuracies[gesture_name]
        count = gesture_counts.get(gesture_name, 0)
        
        status = "✓✓ Excellent" if acc >= 0.95 else ("✓ Good" if acc >= 0.85 else ("○ Fair" if acc >= 0.75 else "✗ Poor"))
        
        print(f"  {gesture_name:15s}: {acc:6.2%}  ({count:3d} samples)  {status}")
    
    print("="*70 + "\n")
    
    # Summary
    print(" SUMMARY:")
    print(f"   • ML Model Type: {ml_name}")
    if train_acc > 0:
        print(f"   • Training Accuracy: {train_acc*100:.2f}%")
    print(f"   • Test Accuracy: {ml_accuracy*100:.2f}%")
    print(f"   • Total Test Samples: {len(X)}")
    print(f"   • Gestures Tested: {len(gesture_counts)}")
    
    # Gestures with low accuracy
    low_acc_gestures = [name for name, acc in gesture_accuracies.items() if acc < 0.80]
    if low_acc_gestures:
        print(f"\n⚠ Gestures needing more training data:")
        for name in low_acc_gestures:
            print(f"   • {name}: {gesture_accuracies[name]*100:.1f}% (collect more samples)")
    
    print("\n" + "="*70)
    print(" For detailed comparison with actual rule-based testing:")
    print("   Create and run: python compare_models.py")
    print("="*70 + "\n")

if __name__ == "__main__":
    quick_compare()
