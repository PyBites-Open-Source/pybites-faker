from operator import itemgetter
import pickle

import feedparser
import requests

from .constants import (FAKE_DATA_CACHE,
                        BITE_FEED,
                        BLOG_FEED,
                        Bite, Article)
from .data import PyBitesData


def _get_bites():
    resp = requests.get(BITE_FEED)
    for row in resp.json():
        attrs = itemgetter("number", "title", "level")(row)
        yield Bite(*attrs)


def _get_articles():
    feed = feedparser.parse(BLOG_FEED)
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
