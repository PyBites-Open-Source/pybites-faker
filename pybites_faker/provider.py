import random

from faker.providers import BaseProvider

from .exceptions import NoDataForCriteria
from .caching import create_pb_data_object
from .static_data import FOUNDERS, START_DATE, TODAY


class PyBitesProvider(BaseProvider):

    def __init__(self, *args, **kwargs):
        self.data = create_pb_data_object()
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
