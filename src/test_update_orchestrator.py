import os
os.environ['DB_NAME'] = 'helldivers2_test'
from update_orchestrator import UpdateOrchestrator
from config import Config, setup_logging
from test_utils import clean_test_db, assert_using_test_db


def main():
    assert_using_test_db()
    clean_test_db()
    # Set up config and logging
    config = Config()
    logger = setup_logging(config)

    orchestrator = UpdateOrchestrator(config)
    print('Running UpdateOrchestrator...')
    success = orchestrator.run_update()
    print('UpdateOrchestrator Success:', success)
    clean_test_db()

if __name__ == "__main__":
    main() 