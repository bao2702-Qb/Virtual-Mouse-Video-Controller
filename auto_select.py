"""
Auto Mode Selection - Wrapper
"""
import sys
import os

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import and run
from auto_select_mode import AutoModeSelector

if __name__ == "__main__":
    selector = AutoModeSelector()
    result = selector.select_best_mode()
    
    if result:
        print(f"\n✓ Selected mode: {result['selected_mode'].upper()}")
        print(f"  ML: {result['ml_accuracy']*100:.2f}%")
        print(f"  Rule: {result['rule_accuracy']*100:.2f}%")
        print(f"\nRun: python run_app.py")
