# Chuột Ảo + Điều Khiển Video (Nhận Diện Cử Chỉ với Python & OpenCV)

Hệ thống điều khiển chuột ảo và phát video dựa trên Python sử dụng cử chỉ tay được chụp qua webcam. Dự án này sử dụng MediaPipe để theo dõi bàn tay, OpenCV để xử lý hình ảnh, và PyAutoGUI để điều khiển chuột.



## Kho Mã Nguồn

```bash

cd Virtual-Mouse-Video-Controller
```

## Tính Năng

### Tính Năng Cơ Bản
- **Điều khiển con trỏ chuột** bằng chuyển động ngón tay
- **Thực hiện click** bằng cử chỉ ngón tay
- **Điều khiển phát video** (tua tiến/lùi) bằng cử chỉ ngón cái
- **Điều khiển âm lượng** bằng cử chỉ nhiều ngón tay
- **Chuyển video tiếp theo** bằng cử chỉ điều hướng
- Di chuyển con trỏ mượt mà với độ làm mịn có thể cấu hình
- Hiển thị theo dõi bàn tay theo thời gian thực
- Hiển thị FPS

### Tính Năng Nâng Cao
- **Nhận diện cử chỉ bằng Machine Learning** (Random Forest, SVM, MLP)
- **Thu thập dữ liệu cử chỉ tự động** để huấn luyện
- **So sánh và chọn model** (huấn luyện tất cả models, lưu model tốt nhất)
- **Dự phòng dựa trên quy tắc** khi không có ML model
- Thời gian chờ cử chỉ có thể cấu hình để ngăn kích hoạt nhầm

## Hướng Dẫn Cử Chỉ

### Cử Chỉ Điều Khiển Chuột
1. **Di Chuyển Con Trỏ** 
   - Giơ **CHỈ ngón trỏ** (ngón cái cụp, các ngón khác cụp)
   - Di chuyển tay để điều khiển vị trí con trỏ
   - Trạng thái: Hiển thị "MOVING" trên màn hình

2. **Click Chuột**
   - Giơ **ngón trỏ và ngón giữa** (ngón cái cụp, ngón áp út và út cụp)
   - Đưa chúng lại gần nhau (khoảng cách < 30 pixels)
   - Khi sẵn sàng click, màn hình hiển thị "CLICK READY"
   - Click được kích hoạt khi khoảng cách < 30 pixels
   - Trạng thái: Hiển thị khoảng cách và "Bring fingers closer" khi chưa đủ gần
   - Thời gian chờ: 0.3 giây giữa các lần click

### Cử Chỉ Điều Khiển Video
1. **Tua Tiến (10 giây)**
   - Cụp tất cả ngón tay **trừ ngón cái**
   - Chỉ ngón cái sang **phải**
   - Trạng thái: Hiển thị "FORWARD" trên màn hình
   - Thời gian chờ: 1 giây giữa các lần thực hiện

2. **Tua Lùi (10 giây)**
   - Cụp tất cả ngón tay **trừ ngón cái**
   - Chỉ ngón cái sang **trái**
   - Trạng thái: Hiển thị "BACKWARD" trên màn hình
   - Thời gian chờ: 1 giây giữa các lần thực hiện

### Cử Chỉ Điều Khiển Âm Lượng
1. **Tăng Âm Lượng**
   - Chỉ ngón cái **SANG TRÁI** (ngang)
   - Giơ **tất cả ngón còn lại** (trỏ, giữa, áp út, út)
   - **Xòe rộng bàn tay** (khoảng cách >80px)
   - Trạng thái: Hiển thị "VOLUME UP" trên màn hình
   - Thời gian chờ: 0.3 giây giữa các lần thực hiện

2. **Giảm Âm Lượng**
   - Chỉ ngón cái **SANG TRÁI** (ngang)
   - Giơ **tất cả ngón còn lại** (trỏ, giữa, áp út, út)
   - **Nắm chặt bàn tay** (khoảng cách <40px)
   - Trạng thái: Hiển thị "VOLUME DOWN" trên màn hình
   - Thời gian chờ: 0.3 giây giữa các lần thực hiện

### Cử Chỉ Điều Hướng
1. **Video Tiếp Theo**
   - Giơ **ngón trỏ, giữa, áp út và út** (ngón cái cụp)
   - Trạng thái: Hiển thị "NEXT VIDEO" trên màn hình
   - Thời gian chờ: 1 giây giữa các lần thực hiện

### Các Trạng Thái Cử Chỉ
- **WAITING**: Khi không phát hiện cử chỉ cụ thể nào
- **MOVING**: Trong khi di chuyển con trỏ
- **CLICK READY**: Khi các ngón tay đủ gần để kích hoạt click
- **FORWARD/BACKWARD**: Trong khi thực hiện điều khiển video
- **VOLUME MODE**: Khi ở cử chỉ điều khiển âm lượng (chờ xòe/nắm)
- **VOLUME UP/DOWN**: Khi hành động âm lượng được kích hoạt
- **NEXT VIDEO**: Khi phát hiện cử chỉ video tiếp theo

## Yêu Cầu Hệ Thống

- Python 3.7 trở lên
- Webcam
- Các gói Python cần thiết:
  ```
  mediapipe==0.10.13
  opencv-python==4.9.0.80
  numpy==1.26.2
  pyautogui==0.9.53
  keyboard==0.13.5
  scikit-learn>=1.0.0
  matplotlib>=3.5.0
  seaborn>=0.12.0
  ```

## Cài Đặt

1. Sao chép kho mã nguồn:
```bash

cd Virtual-Mouse-Video-Controller
```

2. Tạo và kích hoạt môi trường ảo (khuyến nghị):
```bash
# Tạo môi trường ảo
python -m venv venv

# Kích hoạt môi trường ảo
# Trên Windows:
venv\Scripts\activate
# Trên macOS/Linux:
source venv/bin/activate
```

3. Cài đằt các gói cần thiết:
```bash
pip install -r requirements.txt
```

## Cách Sử Dụng

### Sử Dụng Cơ Bản (Không Có ML Model)

1. Chạy chương trình chính:
```bash
python VirtualMouse.py
```

2. Cửa sổ webcam sẽ hiển thị:
   - Bộ đếm FPS ở góc trên-trái
   - Trạng thái cử chỉ hiện tại (MOVING, CLICKING, VOLUME, v.v.)
   - Hiển thị theo dõi bàn tay
   - Trạng thái ngón tay và hướng ngón cái (dùng để debug)
   - Hướng dẫn ở dưới cùng
   - Khung tương tác (hình chữ nhật màu tím)
   - Chế độ phát hiện (Rule-Based hoặc ML Model)

3. Thoát chương trình:
   - Nhấn phím 'ESC' để thoát

### Sử Dụng Nâng Cao (Với ML Model)

Để có khả năng nhận diện cử chỉ tốt hơn, bạn có thể huấn luyện một mô hình Machine Learning:

#### Bước 1: Thu Thập Dữ Liệu Huấn Luyện

```bash
python auto_collect_data.py
```

- Theo hướng dẫn trên màn hình để thực hiện mỗi cử chễ
- Script sẽ tự động thu thập 50+ mẫu cho mỗi cử chỉ
- Các cử chỉ được hỗ trợ: moving, clicking, forward, backward, volume_up, volume_down, next_video, waiting
- Dữ liệu được lưu vào `data/gestures/<tên_cử_chỉ>/`

#### Bước 2: Huấn Luyện Models

**Phương Án A: Sử Dụng Script Python (Khuyến Nghị)**
```bash
python train_model.py
```

- Huấn luyện **cả 3 models**: Random Forest, SVM, MLP
- So sánh độ chính xác của chúng
- **Tự động lưu chỉ model tốt nhất**
- Hiển thị các chỉ số hiệu suất chi tiết

**Phương Án B: Sử Dụng Jupyter Notebook (Cho Trực Quan Hóa)**
```bash
jupyter notebook train_model.ipynb
```

- Huấn luyện tương tác với trực quan hóa
- Biểu đồ cột so sánh hiệu suất model
- Confusion matrix dạng heatmap
- Báo cáo phân loại chi tiết

#### Bước 3: Sử Dụng ML Model

```bash
python VirtualMouse.py
```

- Ứng dụng sẽ tự động phát hiện và tải model đã huấn luyện
- Màn hình sẽ hiển thị "Mode: ML Model" nếu model được tải
- Chuyển về "Mode: Rule-Based" nếu không tìm thấy model

### Hướng Dẫn Quy Trình Huấn Luyện

Xem [TRAINING_GUIDE.md](TRAINING_GUIDE.md) để biết hướng dẫn chi tiết về:
- Cách thu thập dữ liệu cử chỉ chất lượng
- Thực hành tốt nhất cho mỗi cử chỉ
- Hiểu về các chỉ số model
- Khắc phục các vấn đề thường gặp

## Mẹo Để Phát Hiện Tốt Hơn

1. **Ánh Sáng**
   - Đảm bảo điều kiện ánh sáng tốt
   - Tránh ánh sáng ngược mạnh
   - Giữ tay được chiếu sáng tốt

2. **Vị Trí Bàn Tay**
   - Ở trong khung tương tác màu tím
   - Giữ tay cách camera 20-40 cm
   - Thực hiện cử chỉ rõ ràng, có chủ đích

3. **Chuyển Động**
   - Di chuyển mượt mà khi điều khiển con trỏ
   - Đợi thời gian chờ giữa các điều khiển video (1 giây)
   - Đợi thời gian chờ giữa các lần click (0.3 giây)

## Cấu Trúc Dự Án

```
Virtual-Mouse-Video-Controller/
├── VirtualMouse.py              # File ứng dụng chính
├── HandTrackingModule.py        # Triển khai theo dõi bàn tay
├── GestureClassifier.py         # Wrapper ML model cho dự đoán cử chỉ
├── auto_collect_data.py         # Thu thập dữ liệu cử chỉ tự động
├── train_model.py               # Huấn luyện và so sánh tất cả ML models
├── train_model.ipynb            # Jupyter notebook cho huấn luyện tương tác
├── train_workflow.py            # Quy trình huấn luyện tự động
├── requirements.txt             # Các gói Python cần thiết
├── README.md                    # Tài liệu dự án
├── CONTRIBUTING.md              # Hướng dẫn đóng góp
├── TRAINING_GUIDE.md            # Hướng dẫn huấn luyện ML model
├── data/                        # Thư mục dữ liệu huấn luyện
│   └── gestures/                # Mẫu cử chỉ (định dạng JSON)
│       ├── moving/
│       ├── clicking/
│       ├── forward/
│       ├── backward/
│       ├── volume_up/
│       ├── volume_down/
│       ├── next_video/
│       └── waiting/
├── models/                      # ML models đã huấn luyện
│   ├── gesture_model_*.pkl      # Model tốt nhất đã huấn luyện
│   └── model_metadata.json      # Thông tin model và so sánh
└── __pycache__/                 # File cache của Python
```

## Tùy Chỉnh

### Tham Số VirtualMouse.py

Bạn có thể điều chỉnh các tham số khác nhau:

```python
# Cài Đặt Camera
wCam, hCam = 640, 480           # Độ phân giải camera

# Điều Khiển Chuột
frameR = 100                    # Giảm khung (khu vực tương tác)
smootening = 8                  # Độ mượt của con trỏ (cao hơn = mượt hơn)

# Thời Gian Chờ Cử Chỉ (giây)
click_cooldown = 0.3            # Giữa các lần click
gesture_cooldown = 1            # Giữa các hành động video (tiến/lùi)
volume_cooldown = 0.3           # Giữa các thay đổi âm lượng
next_video_cooldown = 1         # Giữa các hành động video tiếp theo

# Ngưỡng Âm Lượng (pixels)
VOLUME_UP_THRESHOLD = 80        # Khoảng cách để kích hoạt tăng âm lượng
VOLUME_DOWN_THRESHOLD = 40      # Khoảng cách để kích hoạt giảm âm lượng

# Cài Đặt ML Model
ml_confidence_threshold = 0.7   # Độ tin cậy tối thiểu để sử dụng dự đoán ML
```

### Tham Số HandTrackingModule.py

```python
# Phát Hiện Bàn Tay
detectionCon = 0.5              # Độ tin cậy phát hiện (0.0 - 1.0)
trackCon = 0.5                  # Độ tin cậy theo dõi (0.0 - 1.0)
maxHands = 1                    # Số lượng bàn tay tối đa cần phát hiện

# Ngưỡng Hướng Ngón Cái
thumb_threshold = 20            # Pixels cho phát hiện hướng ngón cái
```

### Tham Số Huấn Luyện Model

Trong `train_model.py`, bạn có thể tùy chỉnh:

```python
# Random Forest
n_estimators = 100              # Số lượng cây
max_depth = 20                  # Độ sâu cây tối đa
min_samples_split = 5           # Số mẫu tối thiểu để tách

# SVM
C = 1.0                         # Tham số regularization
gamma = 'scale'                 # Hệ số kernel

# MLP Neural Network
hidden_layer_sizes = (128, 64)  # Kiến trúc mạng
max_iter = 500                  # Số vòng lặp tối đa
learning_rate = 'adaptive'      # Lịch trình tốc độ học
```

## Đóng Góp

Chúng tôi chào đón các đóng góp! Vui lòng xem [Hướng Dẫn Đóng Góp](CONTRIBUTING.md) để biết chi tiết về:
- Thiết lập môi trường phát triển
- Hướng dẫn phong cách code
- Gửi pull requests
- Báo cáo vấn đề
- Yêu cầu tính năng
- Hướng dẫn kiểm thử

## Giấy Phép

Dự án này được cấp phép theo Giấy Phép MIT.

## Lời Cảm Ơn

- **MediaPipe** team cho giải pháp theo dõi tay xuất sắc
- **OpenCV** team cho thư viện xử lý thị giác máy tính
- **PyAutoGUI** cho điều khiển chuột và bàn phím
- **scikit-learn** cho các thuật toán machine learning
- **keyboard** library cho mô phỏng phím media
- Tất cả những người đóng góp cho dự án này

## Khắc Phục Sự Cố

### Các Vấn Đề Thường Gặp

1. **Cảnh báo "Model not found"**
   - Điều này bình thường nếu bạn chưa huấn luyện model
   - Ứng dụng sẽ sử dụng phát hiện dựa trên quy tắc
   - Để sử dụng ML model, hãy theo các bước huấn luyện ở trên

2. **Cử chỉ không được phát hiện đúng**
   - Đảm bảo điều kiện ánh sáng tốt
   - Giữ tay trong khung màu tím
   - Thực hiện cử chỉ rõ ràng, có chủ đích
   - Kiểm tra trạng thái ngón tay hiển thị trên màn hình để debug

3. **Điều khiển âm lượng không hoạt động**
   - Đảm bảo ngón cái chỉ **SANG TRÁI** (ngang)
   - Tất cả các ngón khác phải giơ lên
   - Xòe/nắm tay rõ ràng
   - Kiểm tra giá trị khoảng cách hiển thị trên màn hình

4. **Moving/Clicking bị nhầm với Volume**
   - Giữ ngón cái **CỤP** khi moving/clicking
   - Volume yêu cầu ngón cái chỉ TRÁI + tất cả ngón giơ lên
   - Kiểm tra chỉ báo "Thumb" trên màn hình

5. **Lỗi import**
   - Đảm bảo tất cả các package đã được cài đặt: `pip install -r requirements.txt`
   - Sử dụng môi trường ảo để tránh xung đột

6. **Độ chính xác model thấp**
   - Thu thập thêm mẫu huấn luyện (khuyến nghị 50+ mẫu mỗi cử chỉ)
   - Đảm bảo thực hiện cử chỉ nhất quán trong quá trình thu thập dữ liệu
   - Thử các điều kiện ánh sáng khác nhau
   - Kiểm tra confusion matrix để xem cử chỉ nào bị nhầm lẫn

## Mẹo Hiệu Suất

1. **Phát Hiện Tốt Hơn**
   - Sử dụng ánh sáng nhất quán
   - Giữ nền đơn giản và tương phản
   - Thực hiện cử chỉ rõ ràng và có chủ đích
   - Ở trong khung tương tác

2. **FPS Cao Hơn**
   - Giảm độ phân giải camera
   - Sử dụng ít max_hands hơn (đã đặt là 1)
   - Đóng các ứng dụng khác đang sử dụng camera

3. **ML Model Chính Xác Hơn**
   - Thu thập 100+ mẫu cho mỗi cử chỉ
   - Thực hiện cử chỉ từ nhiều góc độ khác nhau
   - Bao gồm các biến thể về kích thước/vị trí tay
   - Sử dụng các điều kiện ánh sáng đa dạng
