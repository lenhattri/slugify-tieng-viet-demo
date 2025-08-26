# tests/test_invariants.py
import unicodedata as ud
import pytest
from slugify import slugify_tieng_viet

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
], ids=[
    "vietnamese_title",
    "weird_dashes_underscores",
    "emoji",
    "latin_accents",
    "empty",
    "only_emoji",
    "already_slug_like",
    "nfd_mixed",
    "em_dash",
    "punctuation_runs",
])
def test_charset_and_hyphen_rules(src):
    out = slugify_tieng_viet(src)
    assert "--" not in out
    assert out == out.strip("-")
    assert all(c.islower() or c.isdigit() or c == "-" for c in out)

def test_nfd_nfc_equivalence():
    s = "Tối ươm mơ"
    nfd = ud.normalize("NFD", s)
    nfc = ud.normalize("NFC", s)
    assert slugify_tieng_viet(nfd) == slugify_tieng_viet(nfc)

@pytest.mark.parametrize("src", [
    "Tôi Thấy Hoa Vàng Trên Cỏ Xanh!!!",
    "  A---B__C   ",
    "Xin chào 🌟🔥",
    "đi-cho-nhanh",
], ids=["title_punct", "dash_underscore", "emoji", "already_slug_like"])
def test_idempotent(src):
    once = slugify_tieng_viet(src)
    twice = slugify_tieng_viet(once)
    assert once == twice
