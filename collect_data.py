"""
Data Collection Script - Wrapper
"""
import sys
import os

# Add scripts to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import and run
from auto_collect_data import main

if __name__ == "__main__":
    main()
