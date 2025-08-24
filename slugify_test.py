# test_slugify.py
import unicodedata as ud
import pytest
from slugify import slugify_tieng_viet

# 30 ca input -> expected slug
@pytest.mark.parametrize("src, expected", [
    ("Tôi Thấy Hoa Vàng Trên Cỏ Xanh", "toi-thay-hoa-vang-tren-co-xanh"),
    ("  A---B__C   ", "a-b-c"),
    ("Xin chào 🌟🔥", "xin-chao"),
    ("Café Übermensch", "cafe-ubermensch"),
    ("", ""),
    ("🔥🔥", ""),
    ("đi-cho-nhanh", "di-cho-nhanh"),
    ("Tối ươm mơ", "toi-uom-mo"),                 # trộn NFD/NFC
    ("Hello—world", "hello-world"),                # em dash
    ("A___B...C", "a-b-c"),
    ("Ký_tự đặc biệt!!!", "ky-tu-dac-biet"),
    ("Đường đua F1 2025", "duong-dua-f1-2025"),
    ("Năm 2020: điều gì?", "nam-2020-dieu-gi"),
    ("   ---   ", ""),
    ("Cờ VN 🇻🇳", "co-vn"),
    ("naïve façade rôle", "naive-facade-role"),
    ("Łódź", "odz"),                               # Ł bị loại, còn "odz"
    ("中文 空格", ""),                               # non-ASCII bị bỏ hết
    ("Русский текст", ""),                         # non-ASCII bị bỏ hết
    ("email@example.com", "email-example-com"),
    ("path/to/file", "path-to-file"),
    ("100% hợp lệ", "100-hop-le"),
    ("C++ vs C#", "c-vs-c"),
    ("   abc", "abc"),
    ("abc   ", "abc"),
    ("--abc--", "abc"),
    ("a—b—c—d", "a-b-c-d"),
    ("a\tb\nc", "a-b-c"),
    ("Sài Gòn – Hà Nội", "sai-gon-ha-noi"),        # en dash
    ("ĐẶC SẢN", "dac-san"),
])
def test_slug_outputs(src, expected):
    assert slugify_tieng_viet(src) == expected


# Các quy tắc bất biến: chỉ [a-z0-9-], không '--', không '-' đầu/cuối
@pytest.mark.parametrize("src", [
    "Tôi Thấy Hoa Vàng Trên Cỏ Xanh",
    "  A---B__C   ",
    "Xin chào 🌟🔥",
    "Café Übermensch",
    "",
    "🔥🔥",
    "đi-cho-nhanh",
    "Tối ươm mơ",
    "Hello—world",
    "A___B...C",
])
def test_charset_and_hyphen_rules(src):
    out = slugify_tieng_viet(src)
    assert "--" not in out
    assert out == out.strip("-")
    assert all(c.islower() or c.isdigit() or c == "-" for c in out)


# NFD/NFC phải cho cùng kết quả
def test_nfd_nfc_equivalence():
    s = "Tối ươm mơ"  # 'ố' ở NFD (ô + dấu) + NFC trộn
    nfd = ud.normalize("NFD", s)
    nfc = ud.normalize("NFC", s)
    assert slugify_tieng_viet(nfd) == slugify_tieng_viet(nfc)


# Idempotence: slugify(slug) == slug
@pytest.mark.parametrize("src", [
    "Tôi Thấy Hoa Vàng Trên Cỏ Xanh!!!",
    "  A---B__C   ",
    "Xin chào 🌟🔥",
    "đi-cho-nhanh",
])
def test_idempotent(src):
    once = slugify_tieng_viet(src)
    twice = slugify_tieng_viet(once)
    assert once == twice


# max_len: cắt “thông minh”, không để '-' ở cuối
@pytest.mark.parametrize("src,max_len,acceptable", [
    ("di-cho-nhanh", 5, {"di-cho", "di"}),      # ưu tiên cắt tại '-'
    ("abcde", 3, {"abc"}),                      # không có '-', cắt cứng
    ("a-b-c", 1, {"a"}),                        # rất ngắn
    ("a-b-c", 2, {"a", "a-b"}),                 # có thể cắt tại '-'
    ("---", 2, {""}),                           # toàn separator → rỗng
    ("hello-world", 11, {"hello-world"}),       # vừa khít
    ("hello-world", 10, {"hello"}),             # cắt tại '-'
])
def test_max_len_behavior(src, max_len, acceptable):
    out = slugify_tieng_viet(src, max_len=max_len)
    assert out in acceptable
    assert not out.endswith("-")
