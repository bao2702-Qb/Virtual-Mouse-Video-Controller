# Quick Start Guide

## Cài đặt nhanh (3 phút)

### 1. Clone & Install
```bash
git clone https://github.com/bao2702-Qb/Virtual-Mouse-Video-Controller.git
cd Virtual-Mouse-Video-Controller
pip install -r requirements.txt
```

### 2. Test camera
```bash
python test_setup.py
```

### 3. Chạy ngay
```bash
python VirtualMouse.py
```

✅ Xong! Hệ thống sẽ dùng Rule-based mode (78% accuracy)

---

## Nâng cấp lên ML Mode (95%+ accuracy)

### Bước 1: Thu thập dữ liệu (5-10 phút)
```bash
python auto_collect_data.py
```
- Chọn gesture (1-8)
- Thực hiện cử chỉ trước camera
- Thu thập ~50-100 mẫu mỗi gesture

### Bước 2: Train models (1-2 phút)
```bash
python train_model.py
```
- Tự động train 3 models
- Chọn model tốt nhất
- Lưu vào `models/`

### Bước 3: Auto-select và chạy
```bash
python run.py
```
HOẶC
```bash
python auto_select_mode.py
python VirtualMouse.py
```

✅ Hệ thống tự động chọn ML mode!

---

## Cử chỉ cơ bản

| Cử chỉ | Thao tác |
|--------|----------|
| 👆 Ngón trỏ | Di chuyển chuột |
| ✌️ Trỏ + giữa gần nhau | Click |
| 👍 Ngón cái phải | Tua tiến 10s |
| 👈 Ngón cái trái | Tua lùi 10s |
| 🖐️ Ngón cái trái + xòe tay | Tăng âm lượng |
| ✊ Ngón cái trái + nắm tay | Giảm âm lượng |
| 🤚 4 ngón (không cái) | Video tiếp theo |

---

## Phím tắt

- **Q**: Thoát
- **M**: Toggle ML ↔ Rule-based
- **ESC**: Thoát

---

## Troubleshooting

**Camera không hoạt động?**
```bash
python test_setup.py
```

**ML model không load?**
```bash
python train_model.py
```

**Reset về mặc định?**
```bash
del model_config.json
```

---

## Tài liệu đầy đủ

- [README.md](README.md) - Hướng dẫn tổng quan
- [AUTO_SELECT_GUIDE.md](AUTO_SELECT_GUIDE.md) - Auto-selection chi tiết
- [TRAINING_GUIDE.md](TRAINING_GUIDE.md) - Training models chi tiết
- [CONTRIBUTING_VI.md](CONTRIBUTING_VI.md) - Đóng góp dự án

---

**Chúc bạn sử dụng vui vẻ! 🎉**
