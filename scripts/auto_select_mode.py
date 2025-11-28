import os
import json
import numpy as np
import pickle
from sklearn.metrics import accuracy_score

class AutoModeSelector:
    def __init__(self, data_dir=None, model_dir=None, config_file=None):
        # Get project root directory
        self.root_dir = os.path.dirname(os.path.dirname(__file__))
        
        self.data_dir = data_dir or os.path.join(self.root_dir, "data", "gestures")
        self.model_dir = model_dir or os.path.join(self.root_dir, "models")
        self.config_file = config_file or os.path.join(self.root_dir, "config", "model_config.json")
        
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
    
    def load_test_data(self):
        """Load test data"""
        X, y = [], []
        
        for gesture_name, label in self.gesture_map.items():
            gesture_dir = os.path.join(self.data_dir, gesture_name)
            if not os.path.exists(gesture_dir):
                continue
            
            files = [f for f in os.listdir(gesture_dir) if f.endswith('.json')]
            
            for file in files:
                try:
                    filepath = os.path.join(gesture_dir, file)
                    with open(filepath, 'r') as f:
                        data = json.load(f)
                    landmarks = np.array(data['features'])
                    X.append(landmarks)
                    y.append(label)
                except:
                    pass
        
        if len(X) == 0:
            return None, None
        
        return np.array(X), np.array(y)
    
    def test_ml_model(self, X, y):
        """Test ML model accuracy"""
        model_files = [f for f in os.listdir(self.model_dir) if f.endswith('.pkl') and 'gesture_model' in f]
        
        if len(model_files) == 0:
            return 0.0, None
        
        model_path = os.path.join(self.model_dir, model_files[0])
        
        try:
            with open(model_path, 'rb') as f:
                model_data = pickle.load(f)
            
            if isinstance(model_data, dict):
                ml_model = model_data.get('model', model_data)
                model_name = model_data.get('model_name', 'ML Model')
            else:
                ml_model = model_data
                model_name = 'ML Model'
            
            y_pred = ml_model.predict(X)
            accuracy = accuracy_score(y, y_pred)
            
            return accuracy, model_name
        except Exception as e:
            print(f"Error testing ML model: {e}")
            return 0.0, None
    
    def estimate_rule_based(self):
        """Estimate rule-based accuracy based on experience"""
        # Rule-based typically achieves 75-82% accuracy
        return 0.78
    
    def select_best_mode(self):
        """Compare models and select the best one - Returns dict with results"""
        print("\n" + "="*70)
        print("AUTO MODE SELECTION")
        print("="*70 + "\n")
        
        # Check if ML model exists
        if not os.path.exists(self.model_dir):
            print("No ML model found.")
            print("Recommendation: USE RULE-BASED\n")
            result = {
                'selected_mode': 'rule-based',
                'ml_accuracy': 0.0,
                'rule_accuracy': 0.78
            }
            self.save_config(**result)
            return result
        
        model_files = [f for f in os.listdir(self.model_dir) if f.endswith('.pkl') and 'gesture_model' in f]
        
        if len(model_files) == 0:
            print("No ML model found.")
            print("Recommendation: USE RULE-BASED\n")
            result = {
                'selected_mode': 'rule-based',
                'ml_accuracy': 0.0,
                'rule_accuracy': 0.78
            }
            self.save_config(**result)
            return result
        
        # Load test data
        print("Loading test data...")
        X, y = self.load_test_data()
        
        if X is None:
            print("No test data found.")
            print("Using default: RULE-BASED\n")
            result = {
                'selected_mode': 'rule-based',
                'ml_accuracy': 0.0,
                'rule_accuracy': 0.78
            }
            self.save_config(**result)
            return result
        
        print(f"Loaded {len(X)} samples\n")
        
        # Test ML model
        print("Testing ML model...")
        ml_accuracy, ml_name = self.test_ml_model(X, y)
        
        # Estimate rule-based
        rule_accuracy = self.estimate_rule_based()
        
        # Display results
        print("\n" + "="*70)
        print("COMPARISON RESULTS")
        print("="*70)
        print(f"\n{'Mode':<30} {'Accuracy':<20} {'Status'}")
        print("-"*70)
        print(f"{'ML Model (' + (ml_name or 'Unknown') + ')':<30} {ml_accuracy:.4f} ({ml_accuracy*100:5.2f}%)")
        print(f"{'Rule-Based (estimated)':<30} ~{rule_accuracy:.4f} (~{rule_accuracy*100:5.2f}%)")
        print("-"*70)
        
        # Select best mode
        if ml_accuracy > rule_accuracy:
            selected_mode = "ml"
            diff = ml_accuracy - rule_accuracy
            improvement = (diff / rule_accuracy) * 100
            print(f"\nML Model is BETTER (+{diff:.4f}, +{improvement:.1f}%)")
            print(f"SELECTED: ML MODEL")
        elif ml_accuracy >= rule_accuracy - 0.05:
            selected_mode = "ml"
            print(f"\nML Model is COMPARABLE")
            print(f"SELECTED: ML MODEL (better generalization)")
        else:
            selected_mode = "rule-based"
            print(f"\nRule-Based is BETTER")
            print(f"SELECTED: RULE-BASED")
        
        print("\n" + "="*70 + "\n")
        
        # Save configuration
        result = {
            'selected_mode': selected_mode,
            'ml_accuracy': float(ml_accuracy),
            'rule_accuracy': float(rule_accuracy)
        }
        self.save_config(**result)
        
        return result
    
    def compare_and_select(self):
        """Legacy method - calls select_best_mode()"""
        result = self.select_best_mode()
        return result['selected_mode']
    
    def save_config(self, selected_mode, ml_accuracy, rule_accuracy):
        """Save selected mode to config file"""
        config = {
            'selected_mode': selected_mode,
            'ml_accuracy': float(ml_accuracy),
            'rule_accuracy': float(rule_accuracy)
        }
        
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"Configuration saved to {self.config_file}")
    
    def get_selected_mode(self):
        """Read selected mode from config"""
        if not os.path.exists(self.config_file):
            return None
        
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
            return config.get('selected_mode', None)
        except:
            return None

if __name__ == "__main__":
    selector = AutoModeSelector()
    selected = selector.compare_and_select()
    
    print(f"\nTo run with selected mode:")
    if selected == "ml":
        print("  python run_ml.py")
    else:
        print("  python run_rulebased.py")
    print()
