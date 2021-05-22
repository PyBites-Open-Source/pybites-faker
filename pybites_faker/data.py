from collections import namedtuple
import pickle
from operator import itemgetter
import os
from pathlib import Path

import feedparser
import requests

TMP = os.getenv("TMP", "/tmp")
PYBITES_FAKER_DIR = Path(os.getenv("PYBITES_FAKER_DIR", TMP))
FAKE_DATA = PYBITES_FAKER_DIR / "pybites-fake-data.pkl"

Bite = namedtuple("Bite", "number title level")
Article = namedtuple("Article", "author title tags")


class PyBitesData:
    pass


def get_bites():
    resp = requests.get("https://codechalleng.es/api/bites/")
    for row in resp.json():
        attrs = itemgetter("number", "title", "level")(row)
        yield Bite(*attrs)


def get_articles():
    feed = feedparser.parse('https://pybit.es/feeds/all.rss.xml')
    for entry in feed.entries:
        tags = [e.term for e in entry.tags]
        yield Article(entry.author, entry.title, tags)


def main():
    pb_data = PyBitesData()

    if FAKE_DATA.exists():
        with open(FAKE_DATA, 'rb') as infile:
            data = pickle.load(infile)
            for k, v in data.items():
                setattr(pb_data, k, v)
    else:
        # cache the data
        data = {
            "bites": list(get_bites()),
            "articles": list(get_articles()),
        }
        with open(FAKE_DATA, 'wb') as outfile:
            pickle.dump(data, outfile)


if __name__ == "__main__":
    main()
