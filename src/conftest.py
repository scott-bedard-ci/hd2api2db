import pytest
from test_utils import clean_test_db, assert_using_test_db

@pytest.fixture(autouse=True)
def setup_test_db_env(monkeypatch):
    monkeypatch.setenv('DB_NAME', 'helldivers2_test')
    monkeypatch.setenv('DB_USER', 'root')
    monkeypatch.setenv('DB_PASSWORD', 'bob')
    monkeypatch.setenv('DB_HOST', 'localhost')
    yield

@pytest.fixture(autouse=True)
def clean_db_before_and_after(request, setup_test_db_env):
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