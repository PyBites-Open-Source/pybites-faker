import re

import pytest

from pybites_faker import (Bite, Article,
                           NoDataForCriteria)

LEVELS = ["intro", "beginner",
          "intermediate", "advanced"]


def test_bite(pb_faker):
    bite = pb_faker.bite()
    assert type(bite) == Bite
    assert bite._fields == ("number", "title", "level")


def test_bite_str(pb_faker):
    bite = pb_faker.bite_str()
    levels = "|".join(level.title() for level in LEVELS)
    pat = re.compile(
        rf"^({levels})\sBite #\d+\.\s.*$")
    assert pat.match(bite)


def test_bite_number(pb_faker):
    # TODO: support ranges?
    bite = pb_faker.bite(number=3)
    assert "3" in str(bite.number)


def test_pandas_bite(pb_faker):
    bite = pb_faker.bite(title="pandas")
    assert "pandas" in bite.title.lower()


@pytest.mark.parametrize("level", LEVELS)
def test_bite_level(pb_faker, level):
    bite = pb_faker.bite(level=level)
    assert bite.level.lower() == level


def test_article(pb_faker):
    article = pb_faker.article()
    assert type(article) == Article
    assert article._fields == ("author", "title", "tags")


def test_pandas_article(pb_faker):
    article = pb_faker.article(title='pandas')
    assert "pandas" in article.title.lower()


def test_pandas_article_mixed_case(pb_faker):
    article = pb_faker.article(title='pAnDaS')
    assert "pandas" in article.title.lower()


def test_mindset_tagged_article(pb_faker):
    article = pb_faker.article(tags='mindset')
    assert "mindset" in str(article.tags).lower()


def test_python_article(pb_faker):
    article = pb_faker.python_article()
    assert "python" in str(article.tags).lower()


def test_wrong_object_searched(pb_faker):
    with pytest.raises(NoDataForCriteria):
        pb_faker.get_one("ninjas")


@pytest.mark.parametrize("method, kwargs", [
    ("bite", {"number1": 1}),
    ("article", {"author2": "darth vader"}),
])
def test_wrong_search_kwargs(pb_faker, method, kwargs):
    with pytest.raises(ValueError):
        getattr(pb_faker, method)(**kwargs)


@pytest.mark.parametrize("method, kwargs", [
    ("bite", {"number": -99}),
    ("bite", {"title": "tim ferriss"}),
    ("bite", {"level": "expert"}),
    ("article", {"author": "darth vader"}),
    ("article", {"title": "some nonsense headline"}),
    ("article", {"tags": "dumb_tag_we_would_not_use"}),
])
def test_no_matching_objects(pb_faker, method, kwargs):
    with pytest.raises(NoDataForCriteria):
        getattr(pb_faker, method)(**kwargs)
