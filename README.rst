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
    $ ipython
    In [1]: from pybites_faker import PyBitesProvider
    In [2]: pbp = PyBitesProvider()
    In [3]: pbp.bite()
    Out[3]: Bite(number=176, title='Create a variable length chessboard', level='Beginner')
    ...

We cache the data in a pickle file which is stored in `/tmp` by default. To store this file somewhere else set the `PYBITES_FAKER_DIR` environment variable, for example::

    $ export PYBITES_FAKER_DIR=$HOME/Downloads/pybites-faker

Then you can get random PyBites objects like::

    >>> from pybites_faker import PyBitesProvider
    >>> pbp = PyBitesProvider()

    # data so far:
    >>> print(pbp.data)
    Articles => 393 objects
    Bites => 328 objects

    # get a random Bite
    >>> pbp.bite()
    Bite(number=228, title='Create a Gravatar URL', level='Intermediate')

    # filter:
    >>> pbp.bite(level="beginner")
    Bite(number=279, title='Armstrong numbers', level='Beginner')
    >>> pbp.bite_str()
    'Intermediate Bite #199. Multiple inheritance (__mro__)'

    # get an article
    >>> pbp.article()
    Article(author='PyBites', title='Code Challenge 29 - Create a Simple Django App', tags=['codechallenges', 'Django', '100DaysOfDjango'])

    # filter:
    >>> art = pbp.article(title="pandas")
    >>> art.author
    'Cedric Sambre'
    >>> art.title
    'Analyzing covid-19 data with pandas and matplotlib'
    >>> art.tags
    ['guest', 'pandas', 'matplotlib', 'data analysis']
    >>> art = pbp.article(tags="mindset")
    >>> art.author
    'Julian'
    >>> art.title
    'Break Fear to Boost Productivity'
    >>> art.tags
    ['productivity', 'motivation', 'mindset', 'fear']

Tests
-----

You can run the tests with::

    poetry run pytest

If you run them often you might want to give it the cache file as argument::

    poetry run pytest --cache=/tmp/pybites-fake-data.pkl
