import os
import json
import hashlib
from pathlib import Path

# ======================================
# Cache Directory
# ======================================

CACHE_DIR = Path("data/cache")

CACHE_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ======================================
# PDF Hash
# ======================================

def get_pdf_hash(pdf_text: str) -> str:
    """
    Creates a unique hash for a PDF.

    Args:
        pdf_text (str)

    Returns:
        str
    """

    return hashlib.md5(
        pdf_text.encode("utf-8")
    ).hexdigest()


# ======================================
# Cache File
# ======================================

def get_cache_file(feature: str, pdf_text: str) -> Path:

    pdf_hash = get_pdf_hash(pdf_text)

    return CACHE_DIR / f"{feature}_{pdf_hash}.json"


# ======================================
# Load Cache
# ======================================

def load_cache(feature: str, pdf_text: str):

    cache_file = get_cache_file(
        feature,
        pdf_text
    )

    if not cache_file.exists():
        return None

    try:

        with open(
            cache_file,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except Exception:

        return None


# ======================================
# Save Cache
# ======================================

def save_cache(feature: str, pdf_text: str, data):

    cache_file = get_cache_file(
        feature,
        pdf_text
    )

    try:

        with open(
            cache_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False
            )

    except Exception:

        pass


# ======================================
# Clear Cache
# ======================================

def clear_cache():

    if not CACHE_DIR.exists():
        return

    for file in CACHE_DIR.glob("*.json"):

        try:
            file.unlink()

        except Exception:
            pass


# ======================================
# Cache Exists
# ======================================

def cache_exists(feature: str, pdf_text: str):

    return get_cache_file(
        feature,
        pdf_text
    ).exists()