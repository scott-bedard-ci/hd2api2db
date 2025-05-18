"""Configuration loading and logging setup utilities."""

import os
import json
import logging
from logging.handlers import RotatingFileHandler

class Config:
    """Load settings from a file or environment variables."""
    def __init__(self, config_file=None):
        self.settings = {
            'DB_HOST': 'localhost',
            'DB_PORT': 3306,
            'DB_NAME': 'helldivers2',
            'DB_USER': None,
            'DB_PASSWORD': None,
            'LOG_LEVEL': 'INFO',
            'LOG_FILE': 'helldivers2_pipeline.log',
            'UPDATE_INTERVAL_HOURS': 24
        }

        # Load from config file if provided
        if config_file and os.path.exists(config_file):
            with open(config_file, 'r') as f:
                file_config = json.load(f)
                self.settings.update(file_config)

        # Override with environment variables
        for key in self.settings.keys():
            env_value = os.environ.get(key)
            if env_value is not None:
                # Convert types as needed
                if isinstance(self.settings[key], int):
                    self.settings[key] = int(env_value)
                else:
                    self.settings[key] = env_value

        # Validate required settings
        required_settings = ['DB_USER', 'DB_PASSWORD', 'DB_NAME']
        missing_settings = [s for s in required_settings if self.settings[s] is None]
        if missing_settings:
            raise ValueError(f"Missing required settings: {', '.join(missing_settings)}")

    def get(self, key, default=None):
        return self.settings.get(key, default)

def setup_logging(config):
    log_level = getattr(logging, config.get('LOG_LEVEL', 'INFO').upper(), logging.INFO)
    log_file = config.get('LOG_FILE')

    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Remove any existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_formatter = logging.Formatter('%(levelname)s - %(message)s')

    # File handler with rotation
    file_handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(log_level)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(log_level)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger 
