# Virtual Mouse + Video Controller

Hệ thống điều khiển chuột và video bằng cử chỉ tay với AI, sử dụng MediaPipe, OpenCV và Machine Learning.

## ✨ Tính năng chính

### Dual-Mode System
- **ML-based**: Nhận diện cử chỉ bằng Machine Learning (Random Forest, SVM, MLP) - 95%+ accuracy
- **Rule-based**: Phương pháp dự phòng dựa trên logic (~78% accuracy)
- **Auto-select**: Tự động chọn chế độ tốt nhất dựa trên so sánh accuracy

### 8 Cử chỉ điều khiển
1. **Moving** - Di chuyển chuột (ngón trỏ)
2. **Clicking** - Click chuột (trỏ + giữa gần nhau)
3. **Forward** - Tua tiến 10s (ngón cái phải)
4. **Backward** - Tua lùi 10s (ngón cái trái)
5. **Volume Up** - Tăng âm lượng (ngón cái trái + xòe bàn tay)
6. **Volume Down** - Giảm âm lượng (ngón cái trái + nắm bàn tay)
7. **Next Video** - Video tiếp theo (4 ngón: trỏ, giữa, áp út, út)
8. **Waiting** - Trạng thái chờ

## 🚀 Quick Start

### 1. Cài đặt
```bash
pip install -r requirements.txt
```

### 2. Chạy ngay (sử dụng Rule-based)
```bash
python VirtualMouse.py
```

### 3. Sử dụng ML Model (khuyến nghị)

**Thu thập dữ liệu:**
```bash
python auto_collect_data.py
```

**Train models:**
```bash
python train_model.py
```

**Tự động chọn và chạy:**
```bash
python auto_select_mode.py
python VirtualMouse.py
```

HOẶC một lệnh:
```bash
python run.py
```

## 📁 Cấu trúc dự án

```
Virtual-Mouse-Video-Controller/
├── VirtualMouse.py           # Main app (dual-mode support)
├── auto_collect_data.py      # Thu thập dữ liệu training
├── train_model.py            # Train 3 ML models, chọn tốt nhất
├── auto_select_mode.py       # So sánh ML vs Rule, chọn tự động
├── run.py                    # Launcher tổng (auto-select + run)
├── GestureClassifier.py      # ML model wrapper
├── HandTrackingModule.py     # MediaPipe hand tracking
├── test_setup.py             # Test camera và dependencies
├── requirements.txt          # Python dependencies
├── model_config.json         # Auto-generated config file
├── data/gestures/            # Training data
├── models/                   # Trained ML models
├── AUTO_SELECT_GUIDE.md      # Hướng dẫn auto-selection chi tiết
├── TRAINING_GUIDE.md         # Hướng dẫn training
└── CONTRIBUTING_VI.md        # Hướng dẫn đóng góp
```

## 📊 Workflow hoàn chỉnh

```
1. Thu thập dữ liệu
   ↓
   python auto_collect_data.py
   ↓
2. Train models
   ↓
   python train_model.py
   ↓
3. Auto-select mode
   ↓
   python auto_select_mode.py
   ↓
4. Chạy app
   ↓
   python VirtualMouse.py
```

## 🎯 Chi tiết cử chỉ

### Di chuyển chuột (Moving)
- Giơ ngón trỏ, cụp các ngón khác
- Di chuyển tay để điều khiển con trỏ

### Click chuột (Clicking)
- Giơ ngón trỏ + giữa
- Đưa gần nhau (< 30px) để click
- Cooldown: 0.3s

### Tua video (Forward/Backward)
- Cụp tất cả trừ ngón cái
- Ngón cái phải → Tua tiến 10s
- Ngón cái trái → Tua lùi 10s
- Cooldown: 1s

### Âm lượng (Volume Up/Down)
- Ngón cái chỉ sang TRÁI
- Giơ 4 ngón còn lại
- Xòe rộng (>120px) → Tăng
- Nắm lại (<70px) → Giảm
- Cooldown: 0.3s

### Video tiếp theo (Next Video)
- Giơ 4 ngón: trỏ, giữa, áp út, út
- Ngón cái cụp
- Cooldown: 1s

## ⚙️ Cấu hình

### Toggle ML/Rule-based
Nhấn phím `M` trong khi chạy để chuyển đổi chế độ

### Auto-select config
File `model_config.json`:
```json
{
  "selected_mode": "ml",
  "ml_accuracy": 0.95,
  "rule_accuracy": 0.78
}
```

## 📈 Kết quả ML Models

| Model | Accuracy | Tốc độ |
|-------|----------|--------|
| Random Forest | ~93% | Nhanh |
| SVM | ~87% | Trung bình |
| MLP Neural Net | ~95% | Nhanh |

**Best model được tự động chọn và lưu**

## 🛠️ Troubleshooting

### ML model không load
```bash
# Train lại model
python train_model.py
```

### Không có dữ liệu training
```bash
# Thu thập dữ liệu
python auto_collect_data.py
```

### Test camera
```bash
python test_setup.py
```

### Reset về mặc định
```bash
del model_config.json
```

## 📚 Tài liệu chi tiết

- [AUTO_SELECT_GUIDE.md](AUTO_SELECT_GUIDE.md) - Hướng dẫn auto-selection
- [TRAINING_GUIDE.md](TRAINING_GUIDE.md) - Hướng dẫn training models
- [CONTRIBUTING_VI.md](CONTRIBUTING_VI.md) - Hướng dẫn đóng góp

## 🔧 Dependencies

```
mediapipe==0.10.13
opencv-python==4.9.0.80
numpy==1.26.2
pyautogui==0.9.53
scikit-learn>=1.3.2
```

## 📄 License

MIT License

## 🤝 Contributing

Xem [CONTRIBUTING_VI.md](CONTRIBUTING_VI.md) để biết chi tiết.

## ⭐ Highlights

- ✅ Dual-mode: ML + Rule-based
- ✅ Auto-select chế độ tốt nhất
- ✅ 95%+ accuracy với ML
- ✅ Real-time gesture detection
- ✅ 8 gestures điều khiển đầy đủ
- ✅ Smooth cursor movement
- ✅ Configurable cooldowns
- ✅ Easy to train và extend

---

**Phát triển bởi bao2702-Qb**
