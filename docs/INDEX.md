# 📚 Documentation Index

Danh sách đầy đủ tài liệu dự án Virtual Mouse Video Controller.

---

## 🚀 Bắt đầu nhanh

### Cho người dùng mới
1. **[QUICKSTART.md](QUICKSTART.md)** ⭐ BẮT ĐẦU TẠI ĐÂY
   - Cài đặt trong 3 phút
   - Chạy ngay lập tức
   - Hướng dẫn từng bước

2. **[README.md](README.md)** 
   - Tổng quan dự án
   - Tính năng chính
   - Workflow hoàn chỉnh

### Cho người muốn train ML
3. **[TRAINING_GUIDE.md](TRAINING_GUIDE.md)**
   - Thu thập dữ liệu
   - Train models
   - Tips & best practices

4. **[AUTO_SELECT_GUIDE.md](AUTO_SELECT_GUIDE.md)**
   - Auto-selection system
   - So sánh ML vs Rule-based
   - Configuration guide

---

## 📖 Tài liệu chi tiết

### Tổng quan kỹ thuật
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)**
  - Architecture overview
  - Design decisions
  - Performance metrics
  - Roadmap

### Lịch sử phát triển
- **[CHANGELOG.md](CHANGELOG.md)**
  - Version history
  - Features added
  - Bug fixes

### Đóng góp
- **[CONTRIBUTING_VI.md](CONTRIBUTING_VI.md)**
  - Coding standards
  - Pull request process
  - Issue guidelines

---

## 💻 Source Code

### Core Files

#### Main Application
- **`VirtualMouse.py`** - Main application with dual-mode support
  - Hand tracking
  - Gesture detection (ML + Rule-based)
  - Mouse & video control
  - ~420 lines

#### ML Components
- **`GestureClassifier.py`** - ML model wrapper
  - Model loading
  - Feature extraction
  - Prediction with confidence
  - ~110 lines

- **`HandTrackingModule.py`** - MediaPipe integration
  - Hand detection
  - Landmark extraction
  - Finger state detection
  - ~120 lines

#### Training Pipeline
- **`auto_collect_data.py`** - Data collection tool
  - Interactive gesture recording
  - Automatic labeling
  - JSON export
  - ~320 lines

- **`train_model.py`** - Model training script
  - Multi-model training (RF, SVM, MLP)
  - Auto-select best model
  - Metrics & reports
  - ~280 lines

- **`auto_select_mode.py`** - Auto-selection system
  - Benchmark ML vs Rule
  - Accuracy comparison
  - Config generation
  - ~200 lines

#### Utilities
- **`run.py`** - Main launcher
  - Auto-select + run workflow
  - ~50 lines

- **`test_setup.py`** - Setup testing
  - Camera test
  - Dependencies check
  - ~140 lines

---

## 📋 Configuration Files

### Python Dependencies
- **`requirements.txt`** - Package dependencies
  ```
  mediapipe==0.10.13
  opencv-python==4.9.0.80
  numpy==1.26.2
  pyautogui==0.9.53
  scikit-learn>=1.3.2
  ```

### Auto-generated
- **`model_config.json`** - Selected mode config
  ```json
  {
    "selected_mode": "ml",
    "ml_accuracy": 0.95,
    "rule_accuracy": 0.78
  }
  ```

### Git
- **`.gitignore`** - Git ignore rules
  - Python cache
  - Virtual env
  - Generated configs

---

## 📂 Directory Structure

```
Virtual-Mouse-Video-Controller/
│
├── 📄 Core Files
│   ├── VirtualMouse.py           # Main app
│   ├── GestureClassifier.py      # ML wrapper
│   └── HandTrackingModule.py     # Hand tracking
│
├── 🤖 Training Pipeline
│   ├── auto_collect_data.py      # Data collection
│   ├── train_model.py            # Model training
│   └── auto_select_mode.py       # Mode selection
│
├── 🛠️ Utilities
│   ├── run.py                    # Main launcher
│   └── test_setup.py             # Setup testing
│
├── 📚 Documentation
│   ├── README.md                 # Main docs
│   ├── QUICKSTART.md             # Quick start
│   ├── TRAINING_GUIDE.md         # Training guide
│   ├── AUTO_SELECT_GUIDE.md      # Auto-select guide
│   ├── PROJECT_SUMMARY.md        # Tech overview
│   ├── CONTRIBUTING_VI.md        # Contributing
│   ├── CHANGELOG.md              # Version history
│   └── INDEX.md                  # This file
│
├── ⚙️ Config
│   ├── requirements.txt          # Dependencies
│   ├── .gitignore                # Git ignore
│   └── model_config.json         # Generated config
│
├── 💾 Data & Models
│   ├── data/gestures/            # Training data
│   └── models/                   # Trained models
│       ├── gesture_model_*.pkl   # ML model
│       └── model_metadata.json   # Model info
│
└── 🐍 Python Environment
    └── venv/                     # Virtual environment
```

---

## 🔍 Quick Navigation

### Tôi muốn...

**...chạy ngay**
→ [QUICKSTART.md](QUICKSTART.md)

**...hiểu cách hoạt động**
→ [README.md](README.md) → [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

**...train ML model**
→ [TRAINING_GUIDE.md](TRAINING_GUIDE.md)

**...hiểu auto-select**
→ [AUTO_SELECT_GUIDE.md](AUTO_SELECT_GUIDE.md)

**...đóng góp code**
→ [CONTRIBUTING_VI.md](CONTRIBUTING_VI.md)

**...xem lịch sử**
→ [CHANGELOG.md](CHANGELOG.md)

**...troubleshoot**
→ [README.md#troubleshooting](README.md#-troubleshooting)

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/bao2702-Qb/Virtual-Mouse-Video-Controller/issues)
- **Discussions**: [GitHub Discussions](https://github.com/bao2702-Qb/Virtual-Mouse-Video-Controller/discussions)

---

**Last Updated**: November 28, 2025
