import subprocess
import sys
import os

print("="*60)
print("STARTING VIRTUAL MOUSE WITH ML MODEL")
print("="*60)
print("\nControls:")
print("  Press 'M' to toggle ML/Rule-Based mode")
print("  Press 'Q' to quit")
print("="*60 + "\n")

# Kiem tra model
if not os.path.exists("models"):
    print("Error: Models directory not found!")
    print("Run: python train_model.py first\n")
    sys.exit(1)

model_files = [f for f in os.listdir("models") if f.endswith('.pkl') and 'gesture_model' in f]
if len(model_files) == 0:
    print("Error: No trained model found!")
    print("Run: python train_model.py first\n")
    sys.exit(1)

print(f"Found model: {model_files[0]}\n")
print("Starting application...\n")

subprocess.run([sys.executable, "VirtualMouse.py"])
