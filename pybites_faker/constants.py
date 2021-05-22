from collections import namedtuple
from os import getenv
from pathlib import Path

TMP = getenv("TMP", "/tmp")
PYBITES_FAKER_DIR = Path(getenv("PYBITES_FAKER_DIR", TMP))
CACHE_FILENAME = "pybites-fake-data.pkl"
FAKE_DATA_CACHE = PYBITES_FAKER_DIR / CACHE_FILENAME
BITE_FEED = "https://codechalleng.es/api/bites/"
BLOG_FEED = "https://pybit.es/feeds/all.rss.xml"

Bite = namedtuple("Bite", "number title level")
Article = namedtuple("Article", "author title tags")
