# AUTO MODE SELECTION - HƯỚNG DẪN SỬ DỤNG

## Tổng quan
Hệ thống tự động so sánh độ chính xác giữa **ML-based** và **Rule-based**, sau đó chọn chế độ tốt nhất để chạy.

---

## Cách chạy

### ⚡ Khởi chạy tự động (KHUYẾN NGHỊ)
```bash
python run.py
```

**Quy trình tự động:**
1. ✓ So sánh ML vs Rule-based trên dữ liệu test
2. ✓ Chọn chế độ có accuracy cao hơn
3. ✓ Lưu config vào `model_config.json`
4. ✓ Khởi chạy `VirtualMouse.py` với chế độ đã chọn

---

### 🔧 Chạy từng bước thủ công

#### Bước 1: So sánh và chọn chế độ
```bash
python auto_select_mode.py
```

**Output mẫu:**
```
======================================================================
AUTO MODE SELECTION
======================================================================

Loading test data...
Loaded 500 samples

Testing ML model...

======================================================================
COMPARISON RESULTS
======================================================================

Mode                           Accuracy             Status
----------------------------------------------------------------------
ML Model (Random Forest)       0.9600 (96.00%)
Rule-Based (estimated)         ~0.7800 (~78.00%)
----------------------------------------------------------------------

ML Model is BETTER (+0.1800, +23.1%)
SELECTED: ML MODEL

======================================================================

Configuration saved to model_config.json
```

#### Bước 2: Chạy VirtualMouse
```bash
python VirtualMouse.py
```

VirtualMouse sẽ tự động đọc `model_config.json` và sử dụng chế độ đã chọn.

---

## Cấu trúc file config

**`model_config.json`:**
```json
{
  "selected_mode": "ml",
  "ml_accuracy": 0.96,
  "rule_accuracy": 0.78
}
```

- **`selected_mode`**: `"ml"` hoặc `"rule-based"`
- **`ml_accuracy`**: Độ chính xác của ML model (0.0 - 1.0)
- **`rule_accuracy`**: Độ chính xác ước lượng của Rule-based (~0.78)

---

## Workflow chi tiết

### 1. Thu thập dữ liệu
```bash
python auto_collect_data.py
```
- Chọn gesture (moving, clicking, forward, backward, volume_up, volume_down, next_video, waiting)
- Thực hiện gesture trước webcam
- Dữ liệu lưu vào `data/gestures/{gesture}/`

### 2. Train ML models
```bash
python train_model.py
```
- Train 3 models: Random Forest, SVM, MLP
- So sánh accuracy và chọn model tốt nhất
- Lưu vào `models/gesture_model_{type}.pkl`

### 3. So sánh ML vs Rule-based
```bash
python auto_select_mode.py
```
- Load dữ liệu test từ `data/gestures/`
- Test ML model với dữ liệu thực
- Ước lượng Rule-based accuracy (~78%)
- Chọn mode tốt hơn và lưu config

### 4. Chạy hệ thống
```bash
python run.py
```
HOẶC
```bash
python VirtualMouse.py
```

---

## Logic chọn chế độ

```python
if ml_accuracy > rule_accuracy:
    selected = "ml"  # ML tốt hơn rõ ràng
    
elif ml_accuracy >= rule_accuracy - 0.05:
    selected = "ml"  # ML gần bằng → chọn ML (generalization tốt hơn)
    
else:
    selected = "rule-based"  # Rule-based tốt hơn
```

---

## Toggle chế độ thủ công

Khi đang chạy `VirtualMouse.py`, nhấn phím **`M`** để chuyển đổi giữa ML và Rule-based:
- **ML Mode**: Hiển thị `Mode: ML (96%)`
- **Rule-based**: Hiển thị `Mode: Rule-Based`

---

## Khắc phục sự cố

### ❌ Lỗi: "No ML model found"
**Nguyên nhân**: Chưa train ML model  
**Giải pháp**:
```bash
python train_model.py
```

### ❌ Lỗi: "No test data found"
**Nguyên nhân**: Chưa có dữ liệu trong `data/gestures/`  
**Giải pháp**:
```bash
python auto_collect_data.py
```

### ❌ Chế độ Rule-based được chọn dù ML accuracy cao
**Nguyên nhân**: Có thể do lỗi trong `auto_select_mode.py`  
**Giải pháp**: Chạy lại
```bash
python auto_select_mode.py
```

### 🔄 Reset về mặc định
Xóa file config:
```bash
del model_config.json
```
VirtualMouse sẽ mặc định sử dụng ML mode.

---

## So sánh các cách chạy

| Cách chạy | Tự động so sánh | Chọn mode tốt nhất | Khuyến nghị |
|-----------|-----------------|-------------------|-------------|
| `python run.py` | ✓ | ✓ | ⭐ TỐT NHẤT |
| `python VirtualMouse.py` | ✗ (dùng config cũ) | ✗ | Chạy nhanh |
| `python run_ml.py` | ✗ | ✗ | Ép dùng ML |
| `python run_rulebased.py` | ✗ | ✗ | Ép dùng Rule |

---

## Kết luận

✅ **Khuyến nghị**: Dùng `python run.py` để tận dụng tối đa hệ thống tự động  
✅ **Linh hoạt**: Toggle bằng phím `M` khi cần  
✅ **Minh bạch**: Xem kết quả so sánh trong console  
✅ **Tối ưu**: Luôn chạy với chế độ có accuracy cao nhất  

---

**Lưu ý**: Hệ thống ưu tiên ML mode nếu accuracy gần bằng Rule-based (trong khoảng 5%) do khả năng generalization tốt hơn.
