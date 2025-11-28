"""
Virtual Mouse Video Controller - Main Launcher
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import and run
from VirtualMouse import main

if __name__ == "__main__":
    main()
