import subprocess
import sys
import os

print("="*60)
print("STARTING VIRTUAL MOUSE WITH RULE-BASED LOGIC")
print("="*60)
print("\nNote: ML Model is disabled")
print("="*60 + "\n")

print("Starting application with Rule-Based mode...\n")

os.environ['USE_ML'] = '0'

subprocess.run([sys.executable, "VirtualMouse.py"])
