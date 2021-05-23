from datetime import date
import re

import pytest

from pybites_faker import (Bite, Article,
                           NoDataForCriteria)

LEVELS = ["intro", "beginner",
          "intermediate", "advanced"]


def test_bite(fake):
    bite = fake.bite()
    assert type(bite) == Bite
    assert bite._fields == ("number", "title", "level")


def test_bite_str(fake):
    bite = fake.bite_str()
    levels = "|".join(level.title() for level in LEVELS)
    pat = re.compile(
        rf"^({levels})\sBite #\d+\.\s.*$")
    assert pat.match(bite)


def test_bite_number(fake):
    # TODO: support ranges?
    bite = fake.bite(number=3)
    assert "3" in str(bite.number)


def test_pandas_bite(fake):
    bite = fake.bite(title="pandas")
    assert "pandas" in bite.title.lower()


@pytest.mark.parametrize("level", LEVELS)
def test_bite_level(fake, level):
    bite = fake.bite(level=level)
    assert bite.level.lower() == level


def test_article(fake):
    article = fake.article()
    assert type(article) == Article
    assert article._fields == ("author", "title", "tags")


def test_pandas_article(fake):
    article = fake.article(title='pandas')
    assert "pandas" in article.title.lower()


def test_pandas_article_mixed_case(fake):
    article = fake.article(title='pAnDaS')
    assert "pandas" in article.title.lower()


def test_mindset_tagged_article(fake):
    article = fake.article(tags='mindset')
    assert "mindset" in str(article.tags).lower()


def test_python_article(fake):
    article = fake.python_article()
    assert "python" in str(article.tags).lower()


def test_wrong_object_searched(fake):
    with pytest.raises(NoDataForCriteria):
        fake.get_one("ninjas")


@pytest.mark.parametrize("method, kwargs", [
    ("bite", {"number1": 1}),
    ("article", {"author2": "darth vader"}),
])
def test_wrong_search_kwargs(fake, method, kwargs):
    with pytest.raises(ValueError):
        getattr(fake, method)(**kwargs)


@pytest.mark.parametrize("method, kwargs", [
    ("bite", {"number": -99}),
    ("bite", {"title": "tim ferriss"}),
    ("bite", {"level": "expert"}),
    ("article", {"author": "darth vader"}),
    ("article", {"title": "some nonsense headline"}),
    ("article", {"tags": "dumb_tag_we_would_not_use"}),
])
def test_no_matching_objects(fake, method, kwargs):
    with pytest.raises(NoDataForCriteria):
        getattr(fake, method)(**kwargs)


def test_pybites_cofounder(fake):
    assert fake.pybites_cofounder() in {"Bob", "Julian"}


def test_pybites_birthday(fake):
    bday = fake.pybites_birthday()
    possible_years = list(range(2016, date.today().year + 1))
    assert bday.day == 19
    assert bday.month == 12
    assert bday.year in possible_years


def test_pybites_tag(fake):
    tags = fake.pybites_tag(n=10)
    assert len(tags) == 10
    # TODO: how to best test the weighting?
    assert all(type(t) is str for t in tags)
