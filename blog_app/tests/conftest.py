# One option is to use their returned values inside your tests. For example:

# import random
# import pytest


# @pytest.fixture
# def random_name():
#     names = ['John', 'Jane', 'Marry']
#     return random.choice(names)


# def test_fixture_usage(random_name):
#     assert random_name

# You can also run part of a fixture before and part after a test using yield instead of return. For example:
# @pytest.fixture
# def some_fixture():
#     # do something before your test
#     yield # test runs here
#     # do something after your test


# Now, add the following fixture to conftest.py, which creates a new database before each test and removes it after:
import os
import tempfile

import pytest

from blog.models import Article


@pytest.fixture(autouse=True)
def database():
    _, file_name = tempfile.mkstemp()
    os.environ['DATABASE_NAME'] = file_name
    Article.create_table(database_name=file_name)
    yield
    os.unlink(file_name)


# The autouse flag is set to True so that it's automatically used by default before (and after) each test in the test suite.
# Since we're using a database for all tests it makes sense to use this flag. That way you don't have to explicitly add the fixture name to every test as a parameter.
