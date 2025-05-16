import pytest
import os
from test_utils import clean_test_db, assert_using_test_db
from dotenv import load_dotenv

load_dotenv()

# Automatically set test DB environment variables for all tests
@pytest.fixture(autouse=True)
def set_test_db_env(monkeypatch):
    # New variables
    monkeypatch.setenv('USE_TEST_DB', 'true')
    monkeypatch.setenv('TEST_DB_HOST', os.getenv('TEST_DB_HOST', 'localhost'))
    monkeypatch.setenv('TEST_DB_PORT', os.getenv('TEST_DB_PORT', '3306'))
    monkeypatch.setenv('TEST_DB_NAME', os.getenv('TEST_DB_NAME', 'helldivers2_test'))
    monkeypatch.setenv('TEST_DB_USER', os.getenv('TEST_DB_USER', 'root'))
    monkeypatch.setenv('TEST_DB_PASSWORD', os.getenv('TEST_DB_PASSWORD', ''))
    # Legacy variables for test isolation (if any code/tests still use them)
    monkeypatch.setenv('DB_HOST', os.getenv('TEST_DB_HOST', 'localhost'))
    monkeypatch.setenv('DB_PORT', os.getenv('TEST_DB_PORT', '3306'))
    monkeypatch.setenv('DB_NAME', os.getenv('TEST_DB_NAME', 'helldivers2_test'))
    monkeypatch.setenv('DB_USER', os.getenv('TEST_DB_USER', 'root'))
    monkeypatch.setenv('DB_PASSWORD', os.getenv('TEST_DB_PASSWORD', ''))
    yield

@pytest.fixture(autouse=True)
def clean_db_before_and_after(request, set_test_db_env):
    if request.node.get_closest_marker('no_db'):
        yield
        return
    assert_using_test_db()
    clean_test_db()
    yield
    clean_test_db()

# Mark all tests as 'fast' by default unless already marked as 'complete'
def pytest_collection_modifyitems(config, items):
    for item in items:
        if 'complete' not in item.keywords:
            item.add_marker('fast') 