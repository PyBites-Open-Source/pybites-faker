from collections import Counter, OrderedDict
from itertools import chain
import random

from faker.providers import BaseProvider

from .exceptions import NoDataForCriteria
from .caching import create_pb_data_object
from .static_data import FOUNDERS, START_DATE, TODAY


class PyBitesProvider(BaseProvider):

    def __init__(self, *args, **kwargs):
        self.data = create_pb_data_object()
        self._tags = None
        super().__init__(*args, **kwargs)

    def get_one(self, pb_obj, **kwargs):
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
        return self.get_one("bites", **kwargs)

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
        return self.get_one("articles", **kwargs)

    def python_article(self):
        return self.article(tags="python")

    def pybites_cofounder(self):
        return random.choice(FOUNDERS)

    def pybites_birthday(self):
        year = random.choice(
            range(START_DATE.year, TODAY.year + 1)
        )
        return START_DATE.replace(year=year)

    def _cache_weighted_tags(self, max_tags=100):
        """Cache blog tags with their weights in an
           OrderedDict (required by Faker's
           random_elements"""
        all_tags = chain.from_iterable(
            [t.lower() for t in article.tags]
            for article in self.data.articles
        )

        common_tags = Counter(
            all_tags).most_common(max_tags)

        num_tags = sum(v for k, v in common_tags)
        self._tags = OrderedDict(
            (k, v/num_tags) for k, v in common_tags
        )

    def pybites_tag(self, n=1):
        """Get one or more weighted blog tags"""
        if self._tags is None:
            self._cache_weighted_tags()

        return self.random_elements(self._tags,
                                    length=n,
                                    unique=True,
                                    use_weighting=True)
