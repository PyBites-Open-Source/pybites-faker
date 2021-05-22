from collections import namedtuple
from operator import itemgetter
import os
from pathlib import Path
import pickle

import feedparser
import requests

TMP = os.getenv("TMP", "/tmp")
PYBITES_FAKER_DIR = Path(os.getenv("PYBITES_FAKER_DIR", TMP))
FAKE_DATA_CACHE = PYBITES_FAKER_DIR / "pybites-fake-data.pkl"

Bite = namedtuple("Bite", "number title level")
Article = namedtuple("Article", "author title tags")


class PyBitesData:
    bites = []
    articles = []

    def __str__(self):
        public_attrs = (name for name in dir(self)
                        if not name.startswith('_'))
        out = []
        for attr in public_attrs:
            items = getattr(self, attr)
            out.append(
                f"{attr.title()} => {len(items)} objects\n")
        return "".join(out)


def _get_bites():
    resp = requests.get("https://codechalleng.es/api/bites/")
    for row in resp.json():
        attrs = itemgetter("number", "title", "level")(row)
        yield Bite(*attrs)


def _get_articles():
    feed = feedparser.parse('https://pybit.es/feeds/all.rss.xml')
    for entry in feed.entries:
        tags = [e.term for e in entry.tags]
        yield Article(entry.author, entry.title, tags)


def _cache_data(cache):
    data = {
        "bites": list(_get_bites()),
        "articles": list(_get_articles()),
    }
    with open(cache, 'wb') as outfile:
        pickle.dump(data, outfile)


def create_pb_data_object(cache=FAKE_DATA_CACHE, force_reload=False):
    if not cache.exists() or force_reload:
        _cache_data(cache)

    pb_data = PyBitesData()

    with open(cache, 'rb') as infile:
        data = pickle.load(infile)
        for k, v in data.items():
            setattr(pb_data, k, v)

    return pb_data


def main():
    data = create_pb_data_object()
    print(str(data))


if __name__ == "__main__":
    main()
