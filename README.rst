PyBites Faker
=============

This package is an extension of the awesome `Faker package <https://faker.readthedocs.io/en/stable/index.html>`_. It brings together a bunch of PyBites objects that can be randomly chosen.

We started with our Bites and articles, but we can add more objects based on our content or personal preferences (think music for example).

Setup
-----

The package is not yet on PyPI, so you can play with it doing the following::

    $ git clone git@github.com:bbelderbos/pybites-faker.git
    $ cd pybites-faker
    $ poetry install
    $ poetry run python
    >>> from faker import Faker
    >>> from pybites_faker import PyBitesProvider
    >>> fake = Faker()
    >>> fake.add_provider(PyBitesProvider)
    >>> fake.bite()
    Bite(number=157, title='Filter out accented characters', level='Intermediate')
    >>> fake.pybites_birthday()
    datetime.date(2019, 12, 19)
    >>> fake.pybites_cofounder()
    'Julian'
    ...

We cache the data in a pickle file which is stored in `/tmp` by default. To store this file somewhere else set the `PYBITES_FAKER_DIR` environment variable, for example::

    $ export PYBITES_FAKER_DIR=$HOME/Downloads/pybites-faker

If the `pybites-faker` directory does not exist it creates it (not recursively though).

Some more functionality (continuation previous REPL session)::

    >>> fake.article()
    Article(author='PyBites', title='Code Challenge 64 - PyCon ES 2019 Marvel Challenge', tags=['code challenge', 'challenges', 'data analysis', 'pycon', 'Marvel', 'data visualization', 'story telling', 'hacktoberfest'])
    >>> art = fake.article()
    >>> art.author
    'PyBites'
    >>> art.title
    'Twitter digest 2017 week 27'
    >>> art.tags[:5]
    ['twitter', 'news', 'tips', 'python', 'pybites']
    >>> fake.article(title="pandas")
    Article(author='Bob', title='Next Time I Will Use Pandas to Parse Html Tables', tags=['BeautifulSoup', 'regex', 'Pandas', 'parsing', 'data', 'data cleaning', 'energy', 'json', 'csv', 'html'])
    >>> fake.bite(level="advanced")
    Bite(number=160, title='15-way Rock Paper Scissors', level='Advanced')

Exceptions
----------

If you filter on the wrong keyword arguments you get a `ValueError`::

    >>> fake.bite(foo='bar')
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "/Users/bbelderbos/code/pybites-faker/pybites_faker/provider.py", line 43, in bite
        return self.get_one("bites", **kwargs)
    File "/Users/bbelderbos/code/pybites-faker/pybites_faker/provider.py", line 25, in get_one
        raise ValueError(
    ValueError: One or more invalid kw args: {'foo': 'bar'}, valid filters are: ('number', 'title', 'level')

Same for article::

    >>> fake.article(foo='bar')
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "/Users/bbelderbos/code/pybites-faker/pybites_faker/provider.py", line 64, in article
        return self.get_one("articles", **kwargs)
    File "/Users/bbelderbos/code/pybites-faker/pybites_faker/provider.py", line 25, in get_one
        raise ValueError(
    ValueError: One or more invalid kw args: {'foo': 'bar'}, valid filters are: ('author', 'title', 'tags')

If you specify wrong filer criteria it raises a `NoDataForCriteria` exception::

    >>> fake.bite(level="expert")
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "/Users/bbelderbos/code/pybites-faker/pybites_faker/provider.py", line 43, in bite
        return self.get_one("bites", **kwargs)
    File "/Users/bbelderbos/code/pybites-faker/pybites_faker/provider.py", line 36, in get_one
        raise NoDataForCriteria(
    pybites_faker.exceptions.NoDataForCriteria: No results for filter criteria: {'level': 'expert'}


Tests
-----

You can run the tests with::

    poetry run pytest

If you want to refresh the cache you can do so with::

    poetry run pytest --refresh_cache
