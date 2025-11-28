# Đóng Góp Cho Dự Án Virtual Mouse + Video Controller

Cảm ơn bạn đã quan tâm đến việc đóng góp cho dự án này! Tài liệu này cung cấp hướng dẫn và thông tin cho những người đóng góp.

## Mục Lục

- [Quy Tắc Ứng Xử](#quy-tắc-ứng-xử)
- [Làm Thế Nào Để Đóng Góp?](#làm-thế-nào-để-đóng-góp)
- [Thiết Lập Môi Trường Phát Triển](#thiết-lập-môi-trường-phát-triển)
- [Hướng Dẫn Phong Cách Code](#hướng-dẫn-phong-cách-code)
- [Hướng Dẫn Kiểm Thử](#hướng-dẫn-kiểm-thử)
- [Quy Trình Pull Request](#quy-trình-pull-request)
- [Báo Cáo Vấn Đề](#báo-cáo-vấn-đề)
- [Yêu Cầu Tính Năng](#yêu-cầu-tính-năng)
- [Câu Hỏi và Thảo Luận](#câu-hỏi-và-thảo-luận)

## Quy Tắc Ứng Xử

Dự án này cam kết cung cấp môi trường thân thiện và hòa nhập cho tất cả những người đóng góp. Bằng cách tham gia, bạn đồng ý:

- Tôn trọng và quan tâm đến người khác
- Sử dụng ngôn ngữ thân thiện và hòa nhập
- Hợp tác và cởi mở với phản hồi mang tính xây dựng
- Tập trung vào điều tốt nhất cho cộng đồng
- Thể hiện sự đồng cảm với các thành viên cộng đồng khác

## Làm Thế Nào Để Đóng Góp?

### Các Loại Đóng Góp

Chúng tôi chào đón nhiều loại đóng góp khác nhau:

- **Báo Cáo Lỗi**: Báo cáo các lỗi và vấn đề bạn gặp phải
- **Yêu Cầu Tính Năng**: Đề xuất các tính năng mới hoặc cải tiến
- **Đóng Góp Code**: Gửi sửa lỗi, tính năng mới hoặc cải tiến
- **Tài Liệu**: Cải thiện hoặc thêm tài liệu
- **Kiểm Thử**: Giúp kiểm thử ứng dụng và báo cáo vấn đề
- **Ví Dụ**: Tạo các script ví dụ hoặc use cases

### Trước Khi Bắt Đầu

1. Kiểm tra các issues và pull requests hiện có để tránh trùng lặp
2. Thảo luận các thay đổi lớn trong một issue trước khi triển khai
3. Đảm bảo các thay đổi của bạn phù hợp với mục tiêu của dự án

## Thiết Lập Môi Trường Phát Triển

### Yêu Cầu Tiên Quyết

- Python 3.7 trở lên
- Git
- Webcam để kiểm thử
- Môi trường ảo (khuyến nghị)
- Jupyter Notebook (tùy chọn, cho huấn luyện tương tác)

### Thiết Lập Phát Triển Cục Bộ

1. **Fork repository**
   ```bash
   # Nhấn nút "Fork" trên GitHub
   # Clone fork của bạn
   git clone https://github.com/TEN_BAN/Virtual-Mouse-Video-Controller.git
   cd Virtual-Mouse-Video-Controller
   ```

2. **Thiết lập môi trường ảo**
   ```bash
   python -m venv venv
   # Trên Windows
   venv\Scripts\activate
   # Trên macOS/Linux
   source venv/bin/activate
   ```

3. **Cài đặt dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Tạo nhánh phát triển**
   ```bash
   git checkout -b feature/ten-tinh-nang-cua-ban
   # hoặc
   git checkout -b fix/sua-loi-cua-ban
   ```

5. **Kiểm thử ứng dụng**
   ```bash
   # Test không có ML model (rule-based)
   python VirtualMouse.py
   
   # Thu thập dữ liệu huấn luyện
   python auto_collect_data.py
   
   # Huấn luyện ML models
   python train_model.py
   
   # Test với ML model
   python VirtualMouse.py
   ```

6. **Tùy chọn: Thiết lập Jupyter Notebook**
   ```bash
   pip install jupyter
   jupyter notebook train_model.ipynb
   ```

## Hướng Dẫn Phong Cách Code

### Phong Cách Code Python

- Tuân theo hướng dẫn [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Sử dụng tên biến và hàm có ý nghĩa
- Giữ các hàm tập trung và dưới 50 dòng khi có thể
- Thêm type hints khi thích hợp
- Sử dụng comments mô tả cho logic phức tạp

### Ví Dụ Về Phong Cách Code Tốt

```python
def tinh_vi_tri_ban_tay(landmarks: List[Tuple[int, int, int]]) -> Tuple[int, int]:
    """
    Tính vị trí trung tâm của bàn tay dựa trên landmarks.
    
    Args:
        landmarks: Danh sách tọa độ (x, y, z) cho các landmarks của bàn tay
        
    Returns:
        Tuple gồm (center_x, center_y)
    """
    if not landmarks:
        return (0, 0)
    
    x_coords = [lm[0] for lm in landmarks]
    y_coords = [lm[1] for lm in landmarks]
    
    center_x = sum(x_coords) // len(x_coords)
    center_y = sum(y_coords) // len(y_coords)
    
    return (center_x, center_y)
```

### Tổ Chức File

- Giữ các chức năng liên quan trong cùng một file
- Sử dụng tên file rõ ràng mô tả mục đích của chúng
- Tổ chức imports: standard library, third-party, local
- Tách biệt các mối quan tâm giữa các modules khác nhau

### Thực Hành Tốt Nhất Cho Machine Learning

1. **Thu Thập Dữ Liệu**
   - Thu thập các mẫu đa dạng (góc độ, ánh sáng khác nhau)
   - Sử dụng hiệu suất cử chỉ nhất quán
   - Lưu dữ liệu ở định dạng JSON chuẩn hóa
   - Bao gồm metadata (timestamp, tên cử chỉ)

2. **Huấn Luyện Model**
   - Luôn huấn luyện nhiều models để so sánh
   - Sử dụng train/test split đúng cách (80/20)
   - Chỉ lưu model có hiệu suất tốt nhất
   - Bao gồm metadata của model (accuracy, features, v.v.)
   - Sử dụng random seeds có thể tái tạo

3. **Feature Engineering**
   - Chuẩn hóa features so với vị trí cổ tay
   - Bao gồm các features dựa trên khoảng cách
   - Duy trì khả năng tương thích ngược với các models hiện có
   - Tài liệu hóa các features mới một cách rõ ràng

4. **Đánh Giá Model**
   - Báo cáo accuracy, precision, recall, F1-score
   - Bao gồm confusion matrix
   - Test trên dữ liệu chưa thấy
   - So sánh với baseline dựa trên quy tắc

### Ví Dụ Code ML Tốt

```python
def trích_xuất_features(lmList: List[List[int]]) -> np.ndarray:
    """
    Trích xuất features đã chuẩn hóa từ landmarks của bàn tay.
    
    Args:
        lmList: Danh sách tọa độ [id, x, y] cho 21 landmarks của bàn tay
        
    Returns:
        Feature vector dưới dạng numpy array
    """
    if len(lmList) < 21:
        return None
    
    # Chuẩn hóa so với cổ tay
    wrist = np.array([lmList[0][1], lmList[0][2]])
    features = []
    
    for lm in lmList:
        rel_x = (lm[1] - wrist[0]) / 640.0
        rel_y = (lm[2] - wrist[1]) / 480.0
        features.extend([rel_x, rel_y])
    
    # Thêm distance features
    for tip_id in [4, 8, 12, 16, 20]:
        tip = np.array([lmList[tip_id][1], lmList[tip_id][2]])
        dist = np.linalg.norm(tip - wrist) / 640.0
        features.append(dist)
    
    return np.array(features)
```

## Hướng Dẫn Kiểm Thử

### Kiểm Thử Thủ Công

Trước khi gửi các thay đổi:

1. **Test chức năng cơ bản**
   - Di chuyển con trỏ chuột (chỉ ngón trỏ)
   - Phát hiện click (ngón trỏ + ngón giữa)
   - Cử chỉ điều khiển video (ngón cái trái/phải)
   - Điều khiển âm lượng (ngón cái trái + tất cả ngón xòe/nắm)
   - Video tiếp theo (tất cả ngón trừ ngón cái)
   - Các điều kiện ánh sáng khác nhau

2. **Test phát hiện cử chỉ**
   - Kiểm tra trạng thái ngón tay hiển thị trên màn hình
   - Xác minh phát hiện hướng ngón cái
   - Test thời gian chờ cử chỉ
   - Đảm bảo không có false positives giữa các cử chỉ tương tự
   - Test chuyển đổi cử chỉ (moving → volume → moving)

3. **Test ML model (nếu có)**
   - Thu thập dữ liệu test cho mỗi cử chỉ
   - Huấn luyện models và kiểm tra accuracy
   - So sánh ML vs phát hiện dựa trên quy tắc
   - Test với kích thước/góc độ tay khác nhau
   - Xác minh việc tải model và fallback

4. **Test các trường hợp đặc biệt**
   - Không phát hiện tay
   - Ánh sáng yếu/thay đổi
   - Chuyển động tay nhanh
   - Nhiều lần thử cử chỉ
   - Tay hiển thị một phần
   - Các hướng tay khác nhau

5. **Test trên các hệ thống khác nhau** (NẾU CÓ THỂ)
   - Windows, macOS, Linux
   - Các phiên bản Python khác nhau (3.7+)
   - Các models webcam khác nhau
   - Các độ phân giải màn hình khác nhau

### Kiểm Thử ML Model

Khi làm việc với các tính năng ML:

1. **Kiểm Thử Thu Thập Dữ Liệu**
   ```bash
   python auto_collect_data.py
   ```
   - Xác minh dữ liệu được lưu đúng cách
   - Kiểm tra định dạng JSON
   - Đảm bảo tất cả các cử chỉ được thu thập
   - Test các chế độ thu thập tự động/thủ công

2. **Kiểm Thử Huấn Luyện Model**
   ```bash
   python train_model.py
   ```
   - Xác minh cả 3 models đều được huấn luyện
   - Kiểm tra so sánh accuracy
   - Đảm bảo model tốt nhất được lưu
   - Xác minh metadata.json được tạo
   - Test với dữ liệu tối thiểu (trường hợp đặc biệt)

3. **Kiểm Thử Tích Hợp Model**
   - Test việc tải model trong VirtualMouse.py
   - Xác minh dự đoán ML được sử dụng
   - Test fallback sang rule-based khi không có model
   - Kiểm tra xử lý ngưỡng confidence
   - Xác minh hiển thị mode (ML Model vs Rule-Based)

### Kiểm Thử Tự Động

Khi có thể, thêm unit tests cho chức năng mới:

```python
import unittest
import numpy as np
from HandTrackingModule import handDetector
from GestureClassifier import GestureClassifier

class TestHandDetector(unittest.TestCase):
    def setUp(self):
        self.detector = handDetector()
    
    def test_phat_hien_ngon_tay_len(self):
        """Test phát hiện ngón tay lên/xuống"""
        # Mock landmark data
        # Test logic
        pass
    
    def test_huong_ngon_cai(self):
        """Test phát hiện hướng ngón cái"""
        pass

class TestGestureClassifier(unittest.TestCase):
    def setUp(self):
        self.classifier = GestureClassifier()
    
    def test_trích_xuất_features(self):
        """Test trích xuất features từ landmarks"""
        pass
    
    def test_du_doan_model(self):
        """Test dự đoán model với dữ liệu mock"""
        pass

if __name__ == '__main__':
    unittest.main()
```

### Kiểm Thử Hiệu Suất

1. **Kiểm Thử FPS**
   - Giám sát FPS trong các cử chỉ khác nhau
   - So sánh hiệu suất ML vs rule-based
   - Test với các độ phân giải camera khác nhau

2. **Kiểm Thử Độ Chính Xác**
   - Ghi lại confusion matrix cho các cử chỉ
   - Test tỷ lệ nhận diện cử chỉ
   - Đo tỷ lệ false positive/negative

3. **Kiểm Thử Độ Trễ**
   - Đo thời gian phản hồi cho mỗi cử chỉ
   - Test hiệu quả của cooldown
   - Kiểm tra tác động của cursor smoothing

## Quy Trình Pull Request

### Tạo Pull Request

1. **Đảm bảo code của bạn sẵn sàng**
   - Tất cả tests đều pass
   - Code tuân theo hướng dẫn phong cách
   - Tài liệu đã được cập nhật
   - Không còn debugging code

2. **Viết mô tả rõ ràng**
   - Những thay đổi đã được thực hiện
   - Tại sao cần các thay đổi
   - Cách test các thay đổi
   - Bất kỳ breaking changes nào

3. **Gửi PR**
   - Sử dụng tên nhánh mô tả
   - Tham chiếu đến các issues liên quan
   - Yêu cầu reviews từ maintainers

### Mẫu PR

```markdown
## Mô Tả
Mô tả ngắn gọn về các thay đổi

## Loại Thay Đổi
- [ ] Sửa lỗi
- [ ] Tính năng mới
- [ ] Cử chỉ mới
- [ ] Cải tiến ML model
- [ ] Cập nhật tài liệu
- [ ] Refactoring code
- [ ] Cải thiện hiệu suất

## Cử Chỉ Bị Ảnh Hưởng (nếu có)
- [ ] Moving
- [ ] Clicking
- [ ] Forward/Backward
- [ ] Volume Up/Down
- [ ] Next Video
- [ ] Waiting
- [ ] Cử chỉ mới: _______

## Kiểm Thử
- [ ] Kiểm thử thủ công hoàn thành
- [ ] Đã test với phát hiện rule-based
- [ ] Đã test với ML model
- [ ] Unit tests đã thêm/cập nhật
- [ ] Đã test trên các platforms khác nhau
- [ ] Dữ liệu cử chỉ đã thu thập và test
- [ ] Độ chính xác model đã được xác nhận (nếu có thay đổi ML)

## Tác Động ML Model (nếu có)
- [ ] Yêu cầu huấn luyện lại model
- [ ] Features mới đã thêm vào model
- [ ] Độ chính xác model cải thiện: ____%
- [ ] Tương thích ngược với các models hiện có

## Checklist
- [ ] Code tuân theo hướng dẫn phong cách
- [ ] Đã tự review
- [ ] Tài liệu đã cập nhật
- [ ] README.md đã cập nhật (nếu cần)
- [ ] TRAINING_GUIDE.md đã cập nhật (nếu cần)
- [ ] Không còn debugging code
- [ ] requirements.txt đã cập nhật (nếu cần)
```

## Báo Cáo Vấn Đề

### Mẫu Báo Cáo Lỗi

Khi báo cáo lỗi, vui lòng bao gồm:

```markdown
**Mô Tả Lỗi**
Mô tả rõ ràng về vấn đề

**Các Bước Tái Hiện**
1. Bước 1
2. Bước 2
3. Bước 3

**Hành Vi Mong Đợi**
Điều gì nên xảy ra

**Hành Vi Thực Tế**
Điều gì thực sự xảy ra

**Môi Trường**
- OS: [ví dụ: Windows 10, macOS 12.0]
- Phiên Bản Python: [ví dụ: 3.8.10]
- Phiên Bản Packages: [từ requirements.txt]
- Phần Cứng: [ví dụ: model webcam]

**Thông Tin Bổ Sung**
Screenshots, error messages, logs
```

### Hướng Dẫn Issue

- Sử dụng tiêu đề mô tả
- Bao gồm error messages liên quan
- Cung cấp các bước tái hiện
- Đề cập môi trường của bạn
- Kiểm tra các issues trùng lặp trước

## Yêu Cầu Tính Năng

### Mẫu Yêu Cầu Tính Năng

```markdown
**Mô Tả Tính Năng**
Mô tả rõ ràng về tính năng được yêu cầu

**Loại Tính Năng**
- [ ] Cử chỉ mới
- [ ] Sửa đổi cử chỉ
- [ ] Cải tiến ML model
- [ ] Nâng cao UI/UX
- [ ] Tối ưu hóa hiệu suất
- [ ] Khác: _______

**Use Case**
Tại sao tính năng này hữu ích

**Đề Xuất Triển Khai**
Bạn nghĩ nó có thể được triển khai như thế nào

**Chi Tiết Cử Chỉ (nếu có)**
- Cấu hình tay: (ngón tay nào lên/xuống)
- Kiểm tra xung đột: (có xung đột với cử chỉ hiện có không?)
- Hành động kích hoạt: (điều gì nên xảy ra)
- Cần cooldown: (có/không)

**Tác Động ML Model (nếu có)**
- Yêu cầu dữ liệu huấn luyện mới
- Cần class cử chỉ mới
- Thay đổi feature engineering
- Tác động accuracy dự kiến

**Các Phương Án Đã Xem Xét**
Các cách tiếp cận khác bạn đã xem xét

**Ngữ Cảnh Bổ Sung**
Bất kỳ thông tin liên quan nào khác
```

## Câu Hỏi và Thảo Luận

### Nhận Trợ Giúp

- Sử dụng GitHub Issues cho câu hỏi
- Cụ thể về vấn đề của bạn
- Bao gồm các code snippets liên quan
- Đề cập những gì bạn đã thử

### Đóng Góp Vào Thảo Luận

- Tôn trọng và mang tính xây dựng
- Cung cấp phản hồi hữu ích
- Chia sẻ kinh nghiệm của bạn
- Giúp đỡ những người đóng góp khác

## Đóng Góp Vào Machine Learning Models

### Cải Thiện Độ Chính Xác Model

1. **Thu Thập Thêm Dữ Liệu**
   - Chạy `auto_collect_data.py` để thêm mẫu
   - Hướng tới 100+ mẫu mỗi cử chỉ
   - Bao gồm các điều kiện đa dạng (ánh sáng, góc độ, backgrounds)

2. **Thử Các Models Khác Nhau**
   - Thử nghiệm với hyperparameters của model
   - Test các thuật toán mới (thêm vào `train_model.py`)
   - So sánh kết quả một cách có hệ thống

3. **Feature Engineering**
   - Thêm features mới vào `GestureClassifier.py`
   - Test tác động lên accuracy
   - Duy trì khả năng tương thích ngược

4. **Chia Sẻ Kết Quả**
   - Báo cáo cải thiện accuracy trong PRs
   - Bao gồm confusion matrices
   - Chia sẻ dữ liệu huấn luyện nếu thích hợp

### Thêm Cử Chỉ Mới

1. **Thiết Kế Cử Chỉ**
   - Chọn cấu hình tay độc đáo
   - Tránh xung đột với các cử chỉ hiện có
   - Làm cho nó dễ thực hiện
   - Tài liệu hóa rõ ràng

2. **Cập Nhật Code**
   - Thêm cử chỉ vào `gesture_map` trong nhiều files:
     - `train_model.py`
     - `GestureClassifier.py`
     - `auto_collect_data.py`
   - Thêm logic phát hiện vào `VirtualMouse.py`
   - Thêm fallback dựa trên quy tắc

3. **Thu Thập Dữ Liệu Huấn Luyện**
   - Sử dụng `auto_collect_data.py`
   - Thu thập tối thiểu 50+ mẫu
   - Thực hiện cử chỉ một cách nhất quán

4. **Kiểm Thử Kỹ Lưỡng**
   - Test nhận diện cử chỉ
   - Kiểm tra false positives
   - Xác minh cooldowns hoạt động
   - Test với cả ML và rule-based modes

5. **Cập Nhật Tài Liệu**
   - Thêm vào README.md Gesture Guide
   - Cập nhật TRAINING_GUIDE.md
   - Bao gồm trong hướng dẫn trên màn hình

## Ghi Nhận

Những người đóng góp sẽ được ghi nhận trong:

- Project README
- Release notes
- Thống kê người đóng góp
- Ghi nhận đặc biệt cho các đóng góp quan trọng

## Nhận Trợ Giúp

Nếu bạn cần trợ giúp với việc đóng góp:

1. Kiểm tra tài liệu hiện có
2. Tìm kiếm các issues hiện có
3. Tạo issue mới với câu hỏi của bạn
4. Tham gia thảo luận cộng đồng

## Giấy Phép

Bằng cách đóng góp cho dự án này, bạn đồng ý rằng các đóng góp của bạn sẽ được cấp phép theo cùng giấy phép với dự án (Giấy Phép MIT).

---

Cảm ơn bạn đã đóng góp cho Dự Án Virtual Mouse + Video Controller! Những đóng góp của bạn giúp dự án này trở nên tốt hơn cho mọi người.
