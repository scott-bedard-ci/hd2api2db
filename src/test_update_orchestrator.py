"""Integration tests for the ``UpdateOrchestrator`` class."""

import pytest
from update_orchestrator import UpdateOrchestrator
from config import Config, setup_logging
from test_utils import clean_test_db, assert_using_test_db

# This is a full integration test and is only run with pytest -m complete
@pytest.mark.complete
def test_update_orchestrator_runs():
    assert_using_test_db()
    clean_test_db()
    config = Config()
    logger = setup_logging(config)
    orchestrator = UpdateOrchestrator(config)
    print('Running UpdateOrchestrator...')
    success = orchestrator.run_update()
    print('UpdateOrchestrator Success:', success)
    clean_test_db()
    assert success is not None 