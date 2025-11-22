#!/usr/bin/env python3
"""
Test script to verify Virtual Mouse setup and dependencies
"""

import sys
import os

def print_header(text):
    print(f"\n{'='*60}")
    print(f" {text}")
    print(f"{'='*60}\n")

def test_dependencies():
    """Test if all required packages are installed"""
    print_header("1. Testing Dependencies")
    
    dependencies = {
        'cv2': 'OpenCV',
        'numpy': 'NumPy',
        'mediapipe': 'MediaPipe',
        'pyautogui': 'PyAutoGUI',
        'keyboard': 'Keyboard',
    }
    
    all_ok = True
    for module_name, display_name in dependencies.items():
        try:
            module = __import__(module_name)
            version = getattr(module, '__version__', 'installed')
            print(f"   [OK] {display_name}: {version}")
        except ImportError as e:
            print(f"   [ERROR] {display_name}: {e}")
            all_ok = False
    
    return all_ok

def test_modules():
    """Test if local modules can be imported"""
    print_header("2. Testing Local Modules")
    
    try:
        import HandTrackingModule as htm
        print("   [OK] HandTrackingModule imported")
        
        # Test handDetector class
        detector = htm.handDetector(maxHands=1)
        print("   [OK] handDetector class initialized")
        
        # Check methods
        methods = ['findHands', 'findPosition', 'fingersUp', 'findDistance']
        for method in methods:
            if hasattr(detector, method):
                print(f"   [OK] Method '{method}' available")
            else:
                print(f"   [ERROR] Method '{method}' NOT found")
                return False
        
        return True
    except Exception as e:
        print(f"   [ERROR] {e}")
        return False

def test_configuration():
    """Test configuration values"""
    print_header("3. Testing Configuration")
    
    try:
        import pyautogui
        import numpy as np
        
        # Camera config
        wCam, hCam = 640, 480
        print(f"   [OK] Camera resolution: {wCam}x{hCam}")
        
        # Frame reduction
        frameR = 100
        print(f"   [OK] Frame reduction: {frameR}")
        
        # Smoothening
        smoothening = 8
        print(f"   [OK] Smoothing factor: {smoothening}")
        
        # Screen size
        wScr, hScr = pyautogui.size()
        print(f"   [OK] Screen size: {wScr}x{hScr}")
        
        # Test interpolation
        test_x = 200
        test_y = 150
        x3 = np.interp(test_x, (frameR, wCam - frameR), (0, wScr))
        y3 = np.interp(test_y, (frameR, hCam - frameR), (0, hScr))
        print(f"   [OK] Interpolation test: ({test_x}, {test_y}) -> ({x3:.1f}, {y3:.1f})")
        
        return True
    except Exception as e:
        print(f"   [ERROR] {e}")
        return False

def test_files():
    """Test if required files exist"""
    print_header("4. Testing Files")
    
    files_to_check = {
        'VirtualMouse.py': 'Main application',
        'HandTrackingModule.py': 'Hand tracking module',
        'requirements.txt': 'Dependencies file',
        'README.md': 'Documentation',
        'video/Virtual-Mouse-Video-Controller.mp4': 'Demo video',
    }
    
    all_ok = True
    for filepath, description in files_to_check.items():
        full_path = os.path.join(os.path.dirname(__file__), filepath)
        if os.path.exists(full_path):
            print(f"   [OK] {description}: {filepath}")
        else:
            print(f"   [ERROR] {description} NOT found: {filepath}")
            all_ok = False
    
    return all_ok

def test_camera_access():
    """Test if camera is accessible"""
    print_header("5. Testing Camera Access")
    
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        
        if cap.isOpened():
            print("   [OK] Camera is accessible")
            cap.release()
            return True
        else:
            print("   [WARNING] Camera is not accessible (may not be available in test environment)")
            return True  # Don't fail if camera is not available
    except Exception as e:
        print(f"   [WARNING] Camera check failed: {e}")
        return True  # Don't fail on camera issues

def main():
    """Run all tests"""
    print("\n")
    print("=" * 60)
    print(" Virtual Mouse Setup Verification")
    print("=" * 60)
    
    tests = [
        ("Dependencies", test_dependencies),
        ("Local Modules", test_modules),
        ("Configuration", test_configuration),
        ("Files", test_files),
        ("Camera Access", test_camera_access),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"   [ERROR] Test failed: {e}")
            results.append((test_name, False))
    
    # Print summary
    print_header("Test Summary")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "PASSED" if result else "FAILED"
        symbol = "[OK]" if result else "[FAIL]"
        print(f"   {symbol} {test_name}: {status}")
    
    print(f"\n   Total: {passed}/{total} tests passed\n")
    
    if passed == total:
        print("   [SUCCESS] All tests passed! You're ready to run VirtualMouse.py")
        return 0
    else:
        print("   [WARNING] Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
