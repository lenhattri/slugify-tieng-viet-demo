# tests/test_suffix.py
import re
import pytest
from slugify import slugify_tieng_viet

def test_suffix_none_default_same_as_base():
    base = slugify_tieng_viet("Mot bai viet")
    explicit = slugify_tieng_viet("Mot bai viet", suffix_mode="none")
    assert base == explicit

def test_suffix_random4_pattern():
    out = slugify_tieng_viet("Một bài viết", suffix_mode="random4")
    assert re.fullmatch(r"[a-z0-9-]+-[0-9a-f]{4}", out)
    assert "--" not in out and out == out.strip("-")

def test_suffix_random6_pattern():
    out = slugify_tieng_viet("Một bài viết", suffix_mode="random6")
    assert re.fullmatch(r"[a-z0-9-]+-[0-9a-f]{6}", out)
    assert "--" not in out and out == out.strip("-")

def test_suffix_date_pattern():
    out = slugify_tieng_viet("abc", suffix_mode="date")
    assert re.fullmatch(r"abc-\d{8}", out)

def test_suffix_datetime_pattern():
    out = slugify_tieng_viet("abc", suffix_mode="datetime")
    assert re.fullmatch(r"abc-\d{12}", out)

def test_suffix_respects_max_len_boundary():
    out = slugify_tieng_viet("abcde", suffix_mode="random4", max_len=10)  # abcde-XXXX
    assert re.fullmatch(r"abcde-[0-9a-f]{4}", out)
    out2 = slugify_tieng_viet("abcde", suffix_mode="random4", max_len=9)   # cắt tại '-'
    assert out2 == "abcde"

def test_suffix_cut_on_hyphen_of_base():
    out = slugify_tieng_viet("hello-world", suffix_mode="random6", max_len=11)
    assert out == "hello-world"

@pytest.mark.parametrize("mode", ["none", "random4", "random6", "date", "datetime"])
def test_suffix_modes_invariants(mode):
    out = slugify_tieng_viet("Tiêu đề: thử nghiệm suffix!", suffix_mode=mode, max_len=80)
    assert "--" not in out
    assert out == out.strip("-")
    assert all(c.islower() or c.isdigit() or c == "-" for c in out)

def test_suffix_empty_input_returns_empty():
    assert slugify_tieng_viet("", suffix_mode="random6") == ""
    assert slugify_tieng_viet("🔥🔥", suffix_mode="date") == ""

def test_suffix_emoji_only_is_empty_even_with_suffix():
    assert slugify_tieng_viet("🤯🤯", suffix_mode="random4") == ""
