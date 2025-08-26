# tests/test_maxlen.py
import pytest
from slugify import slugify_tieng_viet

@pytest.mark.parametrize(
    "src,max_len,acceptable",
    [
        ("di-cho-nhanh", 5, {"di-cho", "di"}),
        ("abcde", 3, {"abc"}),
        ("a-b-c", 1, {"a"}),
        ("a-b-c", 2, {"a", "a-b"}),
        ("---", 2, {""}),
        ("hello-world", 11, {"hello-world"}),
        ("hello-world", 10, {"hello"}),
    ],
    ids=[
        "prefer_cut_on_hyphen",
        "hard_cut_no_hyphen",
        "very_short",
        "short_maybe_keep_hyphen",
        "only_separators",
        "fits_exact",
        "cut_at_hyphen",
    ]
)
def test_max_len_behavior(src, max_len, acceptable):
    out = slugify_tieng_viet(src, max_len=max_len)
    assert out in acceptable
    assert not out.endswith("-")
