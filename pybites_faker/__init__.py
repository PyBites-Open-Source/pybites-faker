from collections import namedtuple
from operator import itemgetter
from os import getenv
from pathlib import Path
import pickle
import random

import feedparser
import requests
from faker.providers import BaseProvider

from .exceptions import NoDataForCriteria


TMP = getenv("TMP", "/tmp")
PYBITES_FAKER_DIR = Path(getenv("PYBITES_FAKER_DIR", TMP))
CACHE_FILENAME = "pybites-fake-data.pkl"
FAKE_DATA_CACHE = PYBITES_FAKER_DIR / CACHE_FILENAME

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


class PyBitesProvider(BaseProvider):

    def __init__(self, data=None):
        self.data = data or create_pb_data_object()

    def _get_one(self, pb_obj, **kwargs):
        data = getattr(self.data, pb_obj, None)
        if data is None:
            raise NoDataForCriteria(
                f"{pb_obj} is not a valid PyBites object"
            )

        first = data[0]
        if bool(set(kwargs.keys()) - set(first._fields)):
            raise ValueError(
                f"One or more invalid kw args: {kwargs}, "
                f"valid filters are: {first._fields}"
            )

        for k, v in kwargs.items():
            data = [row for row in data
                    if str(v).lower() in
                    str(getattr(row, k)).lower()]

        if not data:
            raise NoDataForCriteria(
                f"No results for filter criteria: {kwargs}"
            )

        return random.choice(data)

    def bite(self, **kwargs):
        return self._get_one("bites", **kwargs)

    def bite_str(self):
        bite = self.bite()
        number = str(bite.number).zfill(2)
        return (f"{bite.level} Bite #{number}. "
                f"{bite.title}")

    def intro_bite(self):
        return self.bite(level="intro")

    def beginner_bite(self):
        return self.bite(level="beginner")

    def intermediate_bite(self):
        return self.bite(level="intermediate")

    def advanced_bite(self):
        return self.bite(level="advanced")

    def article(self, **kwargs):
        return self._get_one("articles", **kwargs)

    def python_article(self):
        return self.article(tags="python")


if __name__ == "__main__":
    pbf = PyBitesProvider()
    print(pbf.data)

    from pprint import pprint as pp
    pp(pbf.article(tags='pandas'))
