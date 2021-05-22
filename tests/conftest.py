from pathlib import Path

import pytest

import pybites_faker
from pybites_faker import (CACHE_FILENAME,
                           PyBitesProvider)


def pytest_addoption(parser):
    parser.addoption("--cache", action="store")


@pytest.fixture(scope="session")
def user_cache(pytestconfig):
    return pytestconfig.getoption("cache")


@pytest.fixture(scope="session")
def cache(tmp_path_factory):
    path = tmp_path_factory.mktemp(
        "pybites-fake-data-dir") / CACHE_FILENAME
    return path


@pytest.fixture(scope="session")
def data(user_cache, cache):
    """Need to cache once to work with tmp dir
       and so pickle can actually load the data"""
    if user_cache is not None:
        cache = Path(user_cache)

    force_reload = not cache.exists()
    data = pybites_faker.create_pb_data_object(
        cache=cache,
        force_reload=force_reload)

    return data


@pytest.fixture(scope="session")
def pb_faker(data):
    return PyBitesProvider(data)
