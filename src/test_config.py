import os
import json
import logging
from config import Config, setup_logging

os.environ['DB_NAME'] = 'helldivers2_test'

def test_config_env():
    print('Testing Config loading from environment variables...')
    os.environ['DB_USER'] = 'testuser'
    os.environ['DB_PASSWORD'] = 'testpass'
    os.environ['DB_NAME'] = 'testdb'
    os.environ['LOG_LEVEL'] = 'DEBUG'
    config = Config()
    assert config.get('DB_USER') == 'testuser'
    assert config.get('DB_PASSWORD') == 'testpass'
    assert config.get('DB_NAME') == 'testdb'
    assert config.get('LOG_LEVEL') == 'DEBUG'
    print('Config loaded from environment variables OK')

def test_config_file():
    print('Testing Config loading from config file...')
    config_data = {
        'DB_USER': 'fileuser',
        'DB_PASSWORD': 'filepass',
        'DB_NAME': 'filedb',
        'LOG_LEVEL': 'WARNING',
        'LOG_FILE': 'test_log.log'
    }
    with open('test_config.json', 'w') as f:
        json.dump(config_data, f)
    config = Config('test_config.json')
    assert config.get('DB_USER') == 'fileuser'
    assert config.get('DB_PASSWORD') == 'filepass'
    assert config.get('DB_NAME') == 'filedb'
    assert config.get('LOG_LEVEL') == 'WARNING'
    assert config.get('LOG_FILE') == 'test_log.log'
    os.remove('test_config.json')
    print('Config loaded from config file OK')

def test_logging():
    print('Testing logging setup...')
    # Set required env vars for Config
    os.environ['DB_USER'] = 'loguser'
    os.environ['DB_PASSWORD'] = 'logpass'
    os.environ['DB_NAME'] = 'logdb'
    config = Config()
    logger = setup_logging(config)
    logger.debug('This is a DEBUG message (should appear if LOG_LEVEL=DEBUG)')
    logger.info('This is an INFO message')
    logger.warning('This is a WARNING message')
    logger.error('This is an ERROR message')
    print('Logging test messages sent. Check console and log file.')

def clear_env_vars():
    for var in ['DB_USER', 'DB_PASSWORD', 'DB_NAME', 'LOG_LEVEL']:
        if var in os.environ:
            del os.environ[var]

def main():
    test_config_env()
    clear_env_vars()
    test_config_file()
    test_logging()
    print('All Config and logging tests passed!')

if __name__ == '__main__':
    main() 