import json
import os

CACHE_FILE = "pdf_cache.json"


def load_cache():

    if os.path.exists(CACHE_FILE):

        with open(CACHE_FILE, "r") as f:

            return json.load(f)

    return {}


def save_cache(cache):

    with open(CACHE_FILE, "w") as f:

        json.dump(cache, f, indent=4)


def pdf_exists(pdf_hash):

    cache = load_cache()

    return pdf_hash in cache


def add_pdf(pdf_hash):

    cache = load_cache()

    cache[pdf_hash] = True

    save_cache(cache)