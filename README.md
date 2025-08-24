# Slugify Tiếng Việt

Dự án nhỏ bằng **Python** để chuyển đổi chuỗi tiếng Việt (có dấu, ký tự Unicode phức tạp, emoji, ký tự đặc biệt) thành **slug ASCII an toàn cho URL**.  
Bao gồm:

- `slugify.py` : module xử lý chính (hàm `slugify_tieng_viet`).
- `slugify_test.py` : bộ **unit test** với `pytest` (30+ test case, kiểm tra quy tắc bất biến, max_len…).
- `app.py` : ứng dụng **GUI Tkinter** đơn giản để thử trực tiếp.

---

## Clone dự án

```bash
git clone https://github.com/lenhattri/slugify-tieng-viet-demo.git
cd slugify-tieng-viet-demo
````

---

## Sơ đồ pipeline

Hàm `slugify_tieng_viet` xử lý theo pipeline chuẩn hóa → làm sạch → hậu xử lý.

![Sơ đồ pipeline](sodo.png)

---

## Cài đặt

Yêu cầu:

* Python >= 3.9
* Tkinter (có sẵn trong bản cài Python chuẩn)

Cài thêm `pytest` để chạy unit test:

```bash
pip install pytest
```

---

## Sử dụng module

Ví dụ:

```python
from slugify import slugify_tieng_viet

print(slugify_tieng_viet("Tôi Thấy Hoa Vàng Trên Cỏ Xanh"))
# -> "toi-thay-hoa-vang-tren-co-xanh"

print(slugify_tieng_viet("Xin chào 🌟🔥"))
# -> "xin-chao"

print(slugify_tieng_viet("đi-cho-nhanh", max_len=5))
# -> "di-cho" hoặc "di"
```

---

## Unit Test

File `slugify_test.py` chứa hơn 30 test case với `pytest`.

### Chạy test:

```bash
pytest -q slugify_test.py
```

Ví dụ output:

```
................................................
52 passed in 0.45s
```

---

## Ứng dụng GUI

File `app.py` cung cấp **giao diện Tkinter**:

* Ô nhập “Đầu vào”.
* Ô hiển thị “Đầu ra”.
* Nút **Submit** (hoặc nhấn Enter).
* Nút **Xóa** (sáng lên khi đã có đầu ra).
* Nút toggle **Cấu hình** (`▼ Cấu hình` / `▲ Cấu hình`) để mở/đóng phần config.

  * Trong config có `max_len`.

### Chạy app:

```bash
python app.py
```

---

## Ví dụ cực khó

Input:

```
"  Đầy---ký—tự🤯  cực khó!!!   ŁắM liền – 12₫ @@   "
```

Output:

```
"day-ky-tu-cuc-kho-lam-lien-12"
```

---

## Cấu trúc thư mục

```
.
├── app.py             # GUI Tkinter
├── slugify.py         # Module xử lý slugify_tieng_viet
├── slugify_test.py    # Unit test với pytest
├── sodo.png           # Sơ đồ pipeline
└── README.md          # Tài liệu
```

---

## License

MIT




