"""Command line interface for running and scheduling pipeline updates."""

import argparse
import sys
import os
import fcntl
import time
import logging
from config import Config, setup_logging
from update_orchestrator import UpdateOrchestrator

LOCK_FILE = '/tmp/helldivers2_pipeline.lock'

TABLES = [
    'planet_history',
    'major_orders',
    'campaigns',
    'news',
    'war_status',
    'planets',
]

def create_cli():
    parser = argparse.ArgumentParser(description='Helldivers 2 Data Pipeline')
    parser.add_argument('--config', help='Path to config file')
    parser.add_argument('--update', action='store_true', help='Run a full data update')
    parser.add_argument('--update-war-status', action='store_true', help='Update war status only')
    parser.add_argument('--update-planets', action='store_true', help='Update planets only')
    parser.add_argument('--update-news', action='store_true', help='Update news only')
    parser.add_argument('--update-campaign', action='store_true', help='Update campaign only')
    parser.add_argument('--update-major-orders', action='store_true', help='Update major orders only')
    parser.add_argument('--update-planet-history', action='store_true', help='Update planet history only')
    parser.add_argument('--daemon', action='store_true', help='Run as a daemon with scheduled updates')
    parser.add_argument('--interval', type=int, help='Update interval in hours (default: 24)')
    parser.add_argument('--wipe-db', action='store_true', help='WIPE ALL DATA from the database (requires --force)')
    parser.add_argument('--force', action='store_true', help='Required with --wipe-db to actually wipe the database')
    return parser

def acquire_lock(lock_file):
    """Acquire an exclusive lock to prevent overlapping runs"""
    lock_fd = open(lock_file, 'w')
    try:
        fcntl.lockf(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return lock_fd
    except IOError:
        return None

def release_lock(lock_fd):
    """Release the lock"""
    if lock_fd:
        fcntl.lockf(lock_fd, fcntl.LOCK_UN)
        lock_fd.close()

def run_daemon(orchestrator, config):
    """Run as a daemon with scheduled updates"""
    interval_hours = config.get('UPDATE_INTERVAL_HOURS', 24)
    interval_seconds = interval_hours * 3600
    lock_file = LOCK_FILE

    logger = setup_logging(config)
    logger = logging.getLogger(__name__)
    logger.info(f"Starting daemon mode with {interval_hours} hour update interval")

    while True:
        lock_fd = acquire_lock(lock_file)
        if not lock_fd:
            logger.error("Another instance is already running. Exiting.")
            sys.exit(1)
        try:
            orchestrator.run_update()
        except Exception as e:
            logger.error(f"Error in daemon update: {str(e)}")
        finally:
            release_lock(lock_fd)
        logger.info(f"Sleeping for {interval_hours} hours until next update")
        time.sleep(interval_seconds)

def wipe_db(force, logger):
    if not force:
        print('WARNING: This will wipe ALL data from the database!')
        print('To proceed, re-run with both --wipe-db and --force.')
        return
    from database_manager import DatabaseManager
    db = DatabaseManager()
    conn = db.get_connection()
    cursor = conn.cursor()
    try:
        logger.info('Disabling foreign key checks...')
        cursor.execute('SET FOREIGN_KEY_CHECKS = 0;')
        for table in TABLES:
            logger.info(f'Truncating table: {table}')
            cursor.execute(f'TRUNCATE TABLE {table};')
        cursor.execute('SET FOREIGN_KEY_CHECKS = 1;')
        conn.commit()
        logger.info('All tables wiped. Database is now empty (schema preserved).')
    finally:
        cursor.close()
        conn.close()

def main():
    parser = create_cli()
    args = parser.parse_args()

    # Load config
    config = Config(args.config) if args.config else Config()

    # Setup logging
    setup_logging(config)
    logger = logging.getLogger(__name__)

    # Create orchestrator
    orchestrator = UpdateOrchestrator(config)

    if args.wipe_db:
        wipe_db(args.force, logger)
    elif args.daemon:
        run_daemon(orchestrator, config)
    elif args.update:
        orchestrator.run_update()
    elif args.update_war_status:
        orchestrator.war_status_fetcher.fetch_and_store()
    elif args.update_planets:
        orchestrator.planet_fetcher.fetch_and_store()
    elif args.update_news:
        orchestrator.news_fetcher.fetch_and_store()
    elif args.update_campaign:
        orchestrator.campaign_fetcher.fetch_and_store()
    elif args.update_major_orders:
        orchestrator.major_orders_fetcher.fetch_and_store()
    elif args.update_planet_history:
        orchestrator.planet_history_fetcher.fetch_and_store()
    else:
        parser.print_help()

if __name__ == '__main__':
    main() 
