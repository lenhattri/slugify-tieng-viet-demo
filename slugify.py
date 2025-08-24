# slugify.py
from __future__ import annotations
import re
import unicodedata as ud
from typing import Optional

_NON_ALNUM_RUN = re.compile(r'[^A-Za-z0-9]+')
_HYPHEN_RUN = re.compile(r'-{2,}')
_TRIM_HYPHENS = re.compile(r'^-+|-+$')
_MANUAL_MAP = {"đ": "d", "Đ": "D"}

def _normalize_to_ascii(text: str) -> str:
    if not text:
        return ""

    # 1) Chuẩn hóa NFC
    s = ud.normalize("NFC", text)

    # 2) Map thủ công (đ/Đ → d/D)
    s = "".join(_MANUAL_MAP.get(ch, ch) for ch in s)

    # 2.5) QUAN TRỌNG: map mọi "dash punctuation" Unicode → '-'
    #    (bao gồm – — ‒ ― − …). Dùng category 'Pd' + vài ký tự tương đương.
    DASHLIKE = {
        "\u2010",  # hyphen
        "\u2011",  # non-breaking hyphen
        "\u2012",  # figure dash
        "\u2013",  # en dash
        "\u2014",  # em dash
        "\u2015",  # horizontal bar
        "\u2212",  # minus sign
        "\u2043",  # hyphen bullet
        "\uFE58",  # small em dash
        "\uFE63",  # small hyphen-minus
        "\uFF0D",  # fullwidth hyphen-minus
    }
    s = "".join("-" if (ud.category(ch) == "Pd" or ch in DASHLIKE) else ch for ch in s)

    # 3) NFKD, bỏ dấu kết hợp (Mn)
    s = ud.normalize("NFKD", s)
    s = "".join(ch for ch in s if ud.category(ch) != "Mn")

    # 4) Encode ASCII (bỏ emoji/ký hiệu không ASCII)
    s = s.encode("ascii", "ignore").decode("ascii", "ignore")
    return s

def _collapse_and_clean_tokens(s: str) -> str:
    s = s.lower()
    s = _NON_ALNUM_RUN.sub("-", s)
    s = _HYPHEN_RUN.sub("-", s)
    s = _TRIM_HYPHENS.sub("", s)
    return s

def _smart_cut(slug: str, max_len: int) -> str:
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

def slugify_tieng_viet(text: str, /, *, max_len: Optional[int] = None) -> str:
    if not text:
        return ""
    ascii_text = _normalize_to_ascii(text)
    if not ascii_text:
        return ""
    slug = _collapse_and_clean_tokens(ascii_text)
    if not slug:
        return ""
    if max_len is not None and max_len >= 0:
        slug = _smart_cut(slug, max_len)
    if slug:
        slug = _HYPHEN_RUN.sub("-", slug)
        slug = _TRIM_HYPHENS.sub("", slug)
    return slug

__all__ = ["slugify_tieng_viet"]
