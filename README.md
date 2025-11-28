# Virtual Mouse + Video Controller 🎮

Hệ thống điều khiển chuột và video bằng cử chỉ tay với AI - Dual-mode ML + Rule-based

[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## ✨ Highlights

-  **Dual-Mode**: ML-based (95%+) + Rule-based (78%)
-  **Auto-Select**: Tự động chọn mode tốt nhất
-  **8 Gestures**: Mouse, click, video, volume control
-  **Real-time**: 20-30 FPS with MediaPipe
-  **3 ML Models**: Random Forest, SVM, MLP
-  **Easy Training**: Auto data collection + model comparison

---

##  Quick Start (3 phút)

### 1. Cài đặt
```bash
git clone https://github.com/bao2702-Qb/Virtual-Mouse-Video-Controller.git
cd Virtual-Mouse-Video-Controller
pip install -r config/requirements.txt
```

### 2. Chạy ngay
```bash
python run_app.py
```

 Sẽ dùng Rule-based mode (~78% accuracy)

---

##  Cấu trúc dự án

```
Virtual-Mouse-Video-Controller/
│
├──  Root Files (Quick access)
│   ├── run_app.py          # Chạy app chính
│   ├── collect_data.py     # Thu thập training data
│   ├── train.py            # Train ML models
│   ├── auto_select.py      # Auto-select best mode
│   └── test_setup.py       # Test camera & deps
│
├──  src/ (Core source code)
│   ├── VirtualMouse.py           # Main application
│   ├── GestureClassifier.py      # ML wrapper
│   └── HandTrackingModule.py     # Hand tracking
│
├──  scripts/ (Training pipeline)
│   ├── auto_collect_data.py      # Data collection logic
│   ├── train_model.py            # Training logic
│   └── auto_select_mode.py       # Mode selection logic
│
├──  docs/ (Documentation)
│   ├── README.md                 # Main docs
│   ├── QUICKSTART.md             # Quick start guide
│   ├── INDEX.md                  # Docs navigation
│   ├── AUTO_SELECT_GUIDE.md      # Auto-select guide
│   ├── TRAINING_GUIDE.md         # Training guide
│   ├── PROJECT_SUMMARY.md        # Technical overview
│   ├── CONTRIBUTING_VI.md        # Contributing guide
│   └── CHANGELOG.md              # Version history
│
├──  config/ (Configuration)
│   ├── requirements.txt          # Python dependencies
│   ├── .gitignore                # Git ignore rules
│   └── model_config.json         # Auto-generated config
│
├──  data/ (Training data)
│   └── gestures/
│       ├── moving/
│       ├── clicking/
│       ├── forward/
│       ├── backward/
│       ├── volume_up/
│       ├── volume_down/
│       ├── next_video/
│       └── waiting/
│
└──  models/ (Trained ML models)
    ├── gesture_model_*.pkl       # Best ML model
    └── model_metadata.json       # Model info
```

---

##  Workflow

### Sử dụng Rule-based (Chạy ngay)
```bash
python run_app.py
```

### Nâng cấp lên ML Mode (95%+ accuracy)

**Bước 1: Thu thập dữ liệu**
```bash
python collect_data.py
# Thực hiện các cử chỉ trước camera
# ~50-100 mẫu mỗi gesture
```

**Bước 2: Train models**
```bash
python train.py
# Tự động train 3 models
# Chọn model tốt nhất
```

**Bước 3: Auto-select và chạy**
```bash
python auto_select.py
python run_app.py
```

---

## 🖐️ Cử chỉ điều khiển

| Cử chỉ | Mô tả | Cooldown |
|--------|-------|----------|
| 👆 **Moving** | Ngón trỏ - Di chuyển chuột | - |
| ✌️ **Clicking** | Trỏ + giữa gần nhau (<30px) | 0.3s |
| 👍 **Forward** | Ngón cái phải - Tua tiến 10s | 1s |
| 👈 **Backward** | Ngón cái trái - Tua lùi 10s | 1s |
| 🖐️ **Volume Up** | Ngón cái trái + xòe tay (>120px) | 0.3s |
| ✊ **Volume Down** | Ngón cái trái + nắm tay (<70px) | 0.3s |
| 🤚 **Next Video** | 4 ngón (không cái) | 1s |
| 🤲 **Waiting** | Idle / No gesture | - |

---

## ⚙️ Commands

### Development
```bash
# Test setup
python test_setup.py

# Collect data (10 minutes)
python collect_data.py

# Train models
python train.py

# Auto-select mode
python auto_select.py

# Run app
python run_app.py
```

### Runtime
- **Q / ESC**: Quit
- **M**: Toggle ML ↔ Rule-based

---

##  Performance

| Mode | Accuracy | Speed | Training Required |
|------|----------|-------|-------------------|
| **Rule-based** | ~78% | Fast | ❌ No |
| **ML (Random Forest)** | ~93% | Fast | ✅ Yes |
| **ML (SVM)** | ~87% | Medium | ✅ Yes |
| **ML (MLP)** | ~95% | Fast | ✅ Yes |

**Auto-select**: Tự động chọn mode có accuracy cao nhất

---

## 📚 Documentation

Xem thêm tại [`docs/`](docs/):

- [ INDEX.md](docs/INDEX.md) - Navigation guide
- [ QUICKSTART.md](docs/QUICKSTART.md) - Quick start
- [ TRAINING_GUIDE.md](docs/TRAINING_GUIDE.md) - Training guide
- [ AUTO_SELECT_GUIDE.md](docs/AUTO_SELECT_GUIDE.md) - Auto-selection
- [ PROJECT_SUMMARY.md](docs/PROJECT_SUMMARY.md) - Tech details
- [ CONTRIBUTING_VI.md](docs/CONTRIBUTING_VI.md) - Contributing

---

## 🛠️ Troubleshooting

**Camera không hoạt động?**
```bash
python test_setup.py
```

**ML model không load?**
```bash
python train.py
```

**Reset về mặc định?**
```bash
del config\\model_config.json
```

---

## 🔧 Dependencies

```
mediapipe==0.10.13
opencv-python==4.9.0.80
numpy==1.26.2
pyautogui==0.9.53
scikit-learn>=1.3.2
```

---

## 📄 License

MIT License - see [LICENSE](LICENSE)

---

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING_VI.md](docs/CONTRIBUTING_VI.md)

---

## 👨‍💻 Author

**bao2702-Qb**

---

## ⭐ Star History

If you find this project useful, please give it a star! ⭐

---

**Version**: 2.0.0 | **Last Updated**: November 28, 2025
