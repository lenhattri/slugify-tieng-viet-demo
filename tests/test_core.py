# tests/test_core.py
import pytest
from slugify import slugify_tieng_viet

cases = [
    ("Tôi Thấy Hoa Vàng Trên Cỏ Xanh", "toi-thay-hoa-vang-tren-co-xanh"),
    ("  A---B__C   ", "a-b-c"),
    ("Xin chào 🌟🔥", "xin-chao"),
    ("Café Übermensch", "cafe-ubermensch"),
    ("", ""),
    ("🔥🔥", ""),
    ("đi-cho-nhanh", "di-cho-nhanh"),
    ("Tối ươm mơ", "toi-uom-mo"),
    ("Hello—world", "hello-world"),
    ("A___B...C", "a-b-c"),
    ("Ký_tự đặc biệt!!!", "ky-tu-dac-biet"),
    ("Đường đua F1 2025", "duong-dua-f1-2025"),
    ("Năm 2020: điều gì?", "nam-2020-dieu-gi"),
    ("   ---   ", ""),
    ("Cờ VN 🇻🇳", "co-vn"),
    ("naïve façade rôle", "naive-facade-role"),
    ("Łódź", "odz"),
    ("中文 空格", ""),
    ("Русский текст", ""),
    ("email@example.com", "email-example-com"),
    ("path/to/file", "path-to-file"),
    ("100% hợp lệ", "100-hop-le"),
    ("C++ vs C#", "c-vs-c"),
    ("   abc", "abc"),
    ("abc   ", "abc"),
    ("--abc--", "abc"),
    ("a—b—c—d", "a-b-c-d"),
    ("a\tb\nc", "a-b-c"),
    ("Sài Gòn – Hà Nội", "sai-gon-ha-noi"),
    ("ĐẶC SẢN", "dac-san"),
]

@pytest.mark.parametrize(
    "src,expected",
    cases,
    ids=[f"case_{i+1}" for i in range(len(cases))]
)
def test_slug_outputs(src, expected):
    assert slugify_tieng_viet(src) == expected
