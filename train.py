"""
Model Training Script - Wrapper
"""
import sys
import os

# Add scripts to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))

# Import and run
from train_model import main

if __name__ == "__main__":
    main()
