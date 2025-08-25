# Virtual Mouse + Video Controller (Gesture Recognition with Python & OpenCV)

A Python-based virtual mouse and video playback control system that uses hand gestures captured through your webcam. This project uses MediaPipe for hand tracking, OpenCV for image processing, and AutoPy for mouse control.

## Demo Video

[<video src="video/Virtual-Mouse-Video-Controller.mp4" controls width="600"></video>](https://github.com/user-attachments/assets/1e7b192e-b806-4a31-9d26-0fa94395404a)

Watch the demo video above to see all gestures in action! The video demonstrates:
- Mouse cursor control with index finger
- Click actions with finger gestures
- Video playback control using thumb gestures
- Real-time hand tracking and visual feedback

## Repository

```bash
git clone https://github.com/NaveenDeveloperR/Virtual-Mouse-Video-Controller.git
cd Virtual-Mouse-Video-Controller
```

## Features

- Mouse cursor control using finger movements
- Click actions with finger gestures
- Video playback control with thumb gestures
- Smooth cursor movement with configurable smoothing
- Real-time hand tracking visualization
- FPS display

## Gesture Guide

### Mouse Control Gestures
1. **Move Cursor** 
   - Raise only your index finger
   - Move your hand to control the cursor position
   - Keep other fingers closed
   - Status: Shows "MOVING" on screen

2. **Click Action**
   - Raise both index and middle fingers
   - Bring them close together (< 30 pixels distance)
   - When ready to click, screen shows "CLICK READY"
   - Click triggers when distance < 30 pixels
   - Status: Shows distance and "Bring fingers closer" when not in click range

### Video Control Gestures
1. **Forward Skip (10 seconds)**
   - Close all fingers except thumb
   - Point thumb to the right
   - Status: Shows "FORWARD" on screen
   - Has 1-second cooldown between actions

2. **Backward Skip (10 seconds)**
   - Close all fingers except thumb
   - Point thumb to the left
   - Status: Shows "BACKWARD" on screen
   - Has 1-second cooldown between actions

### Gesture States
- **WAITING**: When no specific gesture is detected
- **MOVING**: During cursor movement
- **CLICK READY**: When fingers are close enough to trigger click
- **FORWARD/BACKWARD**: During video control actions

## Requirements

- Python 3.7 or higher
- Webcam
- Required Python packages:
  ```
  mediapipe==0.10.13
  opencv-python==4.9.0.80
  numpy==1.26.2
  autopy==4.0.0
  keyboard==0.13.5
  ```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/NaveenDeveloperR/Virtual-Mouse-Video-Controller.git
cd Virtual-Mouse-Video-Controller
```

2. Create and activate a virtual environment (recommended):
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the main script:
```bash
python VirtualMouse.py
```

2. The webcam window will show:
   - FPS counter in top-left
   - Current gesture state
   - Hand tracking visualization
   - Instructions at the bottom
   - Interaction frame (purple rectangle)

3. Exit the program:
   - Press 'ESC' key to quit

## Tips for Better Detection

1. **Lighting**
   - Ensure good lighting conditions
   - Avoid strong backlighting
   - Keep hand well-lit

2. **Hand Position**
   - Stay within the purple interaction frame
   - Keep hand 20-40 cm from camera
   - Make clear, deliberate gestures

3. **Movement**
   - Move smoothly for cursor control
   - Wait for cooldown between video controls (1 second)
   - Wait for cooldown between clicks (0.3 seconds)

## Project Structure

```
Virtual-Mouse-Video-Controller/
├── VirtualMouse.py          # Main application file
├── HandTrackingModule.py    # Hand tracking implementation
├── requirements.txt         # Python dependencies
├── README.md               # Project documentation
├── CONTRIBUTING.md         # Contribution guidelines
└── video/                  # Demo videos
    └── Virtual-Mouse-Video-Controller.mp4
```

## Customization

You can adjust various parameters in `VirtualMouse.py`:
```python
wCam, hCam = 640, 480      # Camera resolution
frameR = 100               # Frame Reduction
smoothening = 8            # Cursor smoothening
click_cooldown = 0.3       # Seconds between clicks
gesture_cooldown = 1       # Seconds between video actions
```

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details on:
- Setting up development environment
- Code style guidelines
- Submitting pull requests
- Reporting issues
- Feature requests
- Testing guidelines

## License

This project is licensed under the MIT License.

## Acknowledgments

- MediaPipe team for hand tracking
- OpenCV team for computer vision
- AutoPy team for mouse control
- All contributors to this project
