from faker import Faker
import pytest

from pybites_faker import (FAKE_DATA_CACHE,
                           create_pb_data_object,
                           PyBitesProvider)


def pytest_addoption(parser):
    parser.addoption("--refresh_cache",
                     action="store_true", default=False)


@pytest.fixture(scope="session")
def refresh_cache(pytestconfig):
    return pytestconfig.getoption("refresh_cache")


@pytest.fixture(scope="session")
def cache(tmp_path_factory, refresh_cache):
    if refresh_cache:
        return tmp_path_factory.mktemp(
            "pybites-fake-data-dir") / "data.pkl"
    return FAKE_DATA_CACHE


@pytest.fixture(scope="session")
def data(cache):
    """Need to cache once to work with tmp dir
       and so pickle can actually load the data"""
    return create_pb_data_object(cache=cache)


@pytest.fixture(scope="session")
def fake(data):
    fake = Faker()
    fake.add_provider(PyBitesProvider)
    return fake
