from faker.providers import BaseProvider

from .data import data


class PyBitesProvider(BaseProvider):

    def __init__(self):
        self.data = data

    def bite(self):
        return self.random_element(self.data.bites)

    def article(self):
        return self.random_element(self.data.articles)


if __name__ == "__main__":
    pp = PyBitesProvider()
    breakpoint()
