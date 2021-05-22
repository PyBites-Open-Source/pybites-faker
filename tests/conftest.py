import pytest


def pytest_addoption(parser):
    parser.addoption("--cache", action="store")
