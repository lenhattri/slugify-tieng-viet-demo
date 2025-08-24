# slugify.py
from __future__ import annotations
import re
import unicodedata as ud
from typing import Optional
from datetime import datetime
import secrets

# Regex cơ bản
_NON_ALNUM_RUN = re.compile(r'[^A-Za-z0-9]+')
_HYPHEN_RUN = re.compile(r'-{2,}')
_TRIM_HYPHENS = re.compile(r'^-+|-+$')
_MANUAL_MAP = {"đ": "d", "Đ": "D"}

def _normalize_to_ascii(text: str) -> str:
    """Chuẩn hóa Unicode và lọc về ASCII cơ bản."""
    if not text:
        return ""
    s = ud.normalize("NFC", text)
    s = "".join(_MANUAL_MAP.get(ch, ch) for ch in s)

    DASHLIKE = {
        "\u2010", "\u2011", "\u2012", "\u2013", "\u2014", "\u2015",
        "\u2212", "\u2043", "\uFE58", "\uFE63", "\uFF0D"
    }
    s = "".join("-" if (ud.category(ch) == "Pd" or ch in DASHLIKE) else ch for ch in s)

    s = ud.normalize("NFKD", s)
    s = "".join(ch for ch in s if ud.category(ch) != "Mn")
    s = s.encode("ascii", "ignore").decode("ascii", "ignore")
    return s

def _collapse_and_clean_tokens(s: str) -> str:
    """Thay cụm ký tự không phải chữ/số bằng '-', gộp/trims dấu '-'."""
    s = s.lower()
    s = _NON_ALNUM_RUN.sub("-", s)
    s = _HYPHEN_RUN.sub("-", s)
    s = _TRIM_HYPHENS.sub("", s)
    return s

def _smart_cut(slug: str, max_len: int) -> str:
    """Cắt slug thông minh với max_len, ưu tiên biên từ '-'."""
    if len(slug) <= max_len:
        return slug
    cut = slug.rfind("-", 0, max_len + 1)
    if cut > 0:
        trimmed = slug[:cut].strip("-")
        if trimmed:
            return trimmed
    trimmed = slug[:max_len].rstrip("-")
    while not trimmed and max_len > 0:
        max_len -= 1
        trimmed = slug[:max_len].rstrip("-")
    return trimmed

def _make_suffix(mode: str) -> str:
    """Sinh suffix theo chế độ."""
    mode = (mode or "none").lower()
    if mode == "none":
        return ""
    if mode == "random4":
        return secrets.token_hex(2)  # 4 hex chars
    if mode == "random6":
        return secrets.token_hex(3)  # 6 hex chars
    if mode == "date":
        return datetime.now().strftime("%Y%m%d")
    if mode == "datetime":
        return datetime.now().strftime("%Y%m%d%H%M")
    return ""

def slugify_tieng_viet(
    text: str,
    /,
    *,
    max_len: Optional[int] = None,
    suffix_mode: str = "none",
) -> str:
    """
    Biến chuỗi tiếng Việt/Unicode thành slug ASCII an toàn.

    suffix_mode: none | random4 | random6 | date | datetime
    """
    if not text:
        return ""
    ascii_text = _normalize_to_ascii(text)
    base = _collapse_and_clean_tokens(ascii_text) if ascii_text else ""
    if not base:
        return ""

    suffix = _make_suffix(suffix_mode)
    slug = f"{base}-{suffix}" if suffix else base

    if max_len is not None and max_len >= 0:
        slug = _smart_cut(slug, max_len)

    slug = _HYPHEN_RUN.sub("-", slug)
    slug = _TRIM_HYPHENS.sub("", slug)
    return slug

__all__ = ["slugify_tieng_viet"]
