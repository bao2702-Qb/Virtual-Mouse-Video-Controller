"""
Helper script để chạy toàn bộ workflow training
"""
import os
import sys
import subprocess

def check_dependencies():
    """Kiểm tra dependencies"""
    try:
        import sklearn
        print("✓ scikit-learn installed")
    except ImportError:
        print("✗ scikit-learn not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "scikit-learn==1.3.2"])
        print("✓ scikit-learn installed")

def collect_data(duration=10):
    """Thu thập dữ liệu"""
    print("\n=== STEP 1: Data Collection ===")
    print(f"Collecting data for {duration} minutes...")
    print("Make gestures naturally. Press 'q' to stop early.\n")
    
    try:
        from auto_collect_data import AutoDataCollector
        collector = AutoDataCollector()
        counts = collector.collect(duration_minutes=duration)
        
        total = sum(counts.values())
        print(f"\n✓ Collection complete! Total: {total} samples")
        
        # Check if we have enough data
        min_samples = 50
        low_samples = [g for g, c in counts.items() if c < min_samples]
        if low_samples:
            print(f"\n⚠ Warning: These gestures have less than {min_samples} samples:")
            for g in low_samples:
                print(f"  - {g}: {counts[g]} samples")
            print(f"\nConsider collecting more data for better accuracy.")
        
        return True
    except Exception as e:
        print(f"✗ Error during data collection: {e}")
        return False

def train_model(model_type='random_forest'):
    """Train mô hình"""
    print(f"\n=== STEP 2: Training {model_type} Model ===")
    
    try:
        from train_model import GestureTrainer
        trainer = GestureTrainer()
        model = trainer.train(model_type=model_type)
        
        if model:
            print(f"\n✓ Training complete!")
            return True
        else:
            print(f"\n✗ Training failed!")
            return False
    except Exception as e:
        print(f"✗ Error during training: {e}")
        return False

def main():
    """Main workflow"""
    print("=" * 50)
    print("Gesture Recognition Training Workflow")
    print("=" * 50)
    
    # Check dependencies
    check_dependencies()
    
    # Ask user what to do
    print("\nWhat would you like to do?")
    print("1. Collect data only")
    print("2. Train model only (requires existing data)")
    print("3. Full workflow (collect + train)")
    print("4. Exit")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == "1":
        duration = input("Duration in minutes (default 10): ").strip()
        duration = int(duration) if duration.isdigit() else 10
        collect_data(duration)
    
    elif choice == "2":
        model_type = input("Model type (random_forest/svm/mlp, default random_forest): ").strip()
        model_type = model_type if model_type in ['random_forest', 'svm', 'mlp'] else 'random_forest'
        train_model(model_type)
    
    elif choice == "3":
        duration = input("Collection duration in minutes (default 10): ").strip()
        duration = int(duration) if duration.isdigit() else 10
        
        model_type = input("Model type (random_forest/svm/mlp, default random_forest): ").strip()
        model_type = model_type if model_type in ['random_forest', 'svm', 'mlp'] else 'random_forest'
        
        if collect_data(duration):
            train_model(model_type)
    
    elif choice == "4":
        print("Exiting...")
        return
    
    else:
        print("Invalid choice!")
        return
    
    print("\n" + "=" * 50)
    print("Workflow complete!")
    print("You can now run VirtualMouse.py to use the trained model.")
    print("=" * 50)

if __name__ == "__main__":
    main()

