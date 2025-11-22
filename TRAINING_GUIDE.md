# Hướng dẫn Training Mô hình Gesture Recognition

## Tổng quan

Dự án này hỗ trợ 2 phương pháp nhận diện cử chỉ:
1. **Rule-based** (mặc định): Sử dụng logic if-else dựa trên vị trí ngón tay
2. **ML Model**: Sử dụng mô hình machine learning đã được train

## Cải thiện Logic Rule-based

Logic rule-based đã được cải thiện, đặc biệt cho volume control:
- **Volume Up**: Index + Middle + Ring (không có Pinky) - `[0,1,1,1,0]`
- **Volume Down**: Index + Middle + Pinky (không có Ring) - `[0,1,1,0,1]`

Điều này giúp phân biệt rõ ràng hơn và dễ thực hiện hơn so với phương pháp dựa vào vị trí tay trước đây.

## Quy trình Training Mô hình

### Bước 1: Thu thập Dữ liệu

Chạy script tự động thu thập dữ liệu:

```bash
python auto_collect_data.py [duration_minutes]
```

**Ví dụ:**
```bash
python auto_collect_data.py 10  # Thu thập trong 10 phút
```

**Cách sử dụng:**
1. Script sẽ tự động detect cử chỉ dựa trên rule-based logic
2. Chỉ cần thực hiện các cử chỉ một cách tự nhiên
3. Dữ liệu sẽ được lưu tự động vào thư mục `data/gestures/`
4. Mỗi cử chỉ sẽ được lưu với interval 0.5 giây

**Các cử chỉ cần thu thập:**
- `moving` (0): Chỉ ngón trỏ
- `clicking` (1): Ngón trỏ + ngón giữa gần nhau
- `forward` (2): Chỉ thumb, chỉ sang phải
- `backward` (3): Chỉ thumb, chỉ sang trái
- `volume_up` (4): Index + Middle + Ring
- `volume_down` (5): Index + Middle + Pinky
- `next_video` (6): Index + Middle + Ring + Pinky
- `waiting` (7): Không có cử chỉ cụ thể

**Lưu ý:**
- Thu thập ít nhất 50-100 mẫu cho mỗi cử chỉ
- Cố gắng thu thập trong các điều kiện ánh sáng khác nhau
- Thực hiện cử chỉ ở các góc độ và vị trí khác nhau

### Bước 2: Training Mô hình

Sau khi thu thập đủ dữ liệu, train mô hình:

```bash
python train_model.py [model_type]
```

**Các loại mô hình:**
- `random_forest` (mặc định): Nhanh, chính xác, dễ sử dụng
- `svm`: Support Vector Machine
- `mlp`: Multi-Layer Perceptron (Neural Network)

**Ví dụ:**
```bash
python train_model.py random_forest
python train_model.py svm
python train_model.py mlp
```

**Output:**
- Mô hình được lưu tại: `models/gesture_model_[model_type].pkl`
- Metadata được lưu tại: `models/model_metadata.json`
- Báo cáo accuracy và confusion matrix

### Bước 3: Sử dụng Mô hình

Mô hình sẽ tự động được load khi chạy `VirtualMouse.py`:

```bash
python VirtualMouse.py
```

**Cách hoạt động:**
- Nếu mô hình tồn tại và load thành công → Sử dụng ML Model
- Nếu không → Tự động fallback về Rule-based
- ML Model chỉ được sử dụng khi confidence > 70%
- Nếu confidence thấp → Tự động chuyển về rule-based

## Cấu trúc Thư mục

```
Virtual-Mouse-Video-Controller/
├── VirtualMouse.py              # Main application (đã tích hợp ML)
├── HandTrackingModule.py        # Hand tracking module
├── GestureClassifier.py         # ML model classifier
├── auto_collect_data.py         # Data collection script
├── train_model.py               # Training script
├── data/                        # Dữ liệu training
│   └── gestures/
│       ├── moving/
│       ├── clicking/
│       ├── forward/
│       ├── backward/
│       ├── volume_up/
│       ├── volume_down/
│       ├── next_video/
│       └── waiting/
├── models/                      # Mô hình đã train
│   ├── gesture_model_random_forest.pkl
│   └── model_metadata.json
└── requirements.txt
```

## Tips để Training Tốt Hơn

1. **Thu thập dữ liệu đa dạng:**
   - Nhiều người khác nhau
   - Nhiều điều kiện ánh sáng
   - Nhiều góc độ và vị trí tay

2. **Cân bằng dữ liệu:**
   - Cố gắng thu thập số lượng mẫu tương đương cho mỗi cử chỉ
   - Ít nhất 50-100 mẫu mỗi cử chỉ

3. **Kiểm tra chất lượng:**
   - Xem confusion matrix sau khi train
   - Nếu một cử chỉ bị nhầm lẫn nhiều → Thu thập thêm dữ liệu cho cử chỉ đó

4. **Fine-tuning:**
   - Nếu accuracy thấp, thử các model khác nhau
   - Có thể điều chỉnh threshold confidence trong VirtualMouse.py

## Troubleshooting

**Lỗi: "No data found"**
- Chưa thu thập dữ liệu, chạy `auto_collect_data.py` trước

**Lỗi: "Model not found"**
- Chưa train mô hình, chạy `train_model.py` trước
- Hoặc kiểm tra đường dẫn trong VirtualMouse.py

**Accuracy thấp:**
- Thu thập thêm dữ liệu
- Đảm bảo dữ liệu chất lượng (cử chỉ rõ ràng)
- Thử các model khác nhau

**ML Model không hoạt động:**
- Kiểm tra confidence threshold (mặc định 0.7)
- Kiểm tra xem model có load thành công không
- Hệ thống sẽ tự động fallback về rule-based

## So sánh Rule-based vs ML Model

| Tiêu chí | Rule-based | ML Model |
|----------|------------|----------|
| **Độ chính xác** | Trung bình | Cao (nếu train tốt) |
| **Tốc độ** | Rất nhanh | Nhanh |
| **Cần training** | Không | Có |
| **Khả năng tùy chỉnh** | Dễ | Khó hơn |
| **Xử lý edge cases** | Kém | Tốt hơn |

## Kết luận

- **Bắt đầu**: Sử dụng rule-based (đã được cải thiện)
- **Nâng cao**: Train ML model để có độ chính xác cao hơn
- **Production**: Kết hợp cả hai với fallback mechanism

