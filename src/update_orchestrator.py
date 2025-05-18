from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, Dict
from helldivers_api_client import Helldivers2ApiClient
from database_manager import DatabaseManager
from transformers.war_status_transformer import WarStatusTransformer
from transformers.planet_transformer import PlanetTransformer
from transformers.news_transformer import NewsTransformer
from transformers.campaign_transformer import CampaignTransformer
from transformers.major_order_transformer import MajorOrderTransformer
from transformers.planet_history_transformer import PlanetHistoryTransformer
from war_status_fetcher import WarStatusFetcher
from planet_fetcher import PlanetFetcher
from news_fetcher import NewsFetcher
from campaign_fetcher import CampaignFetcher
from major_orders_fetcher import MajorOrdersFetcher
from planet_history_fetcher import PlanetHistoryFetcher
from transformers.war_info_transformer import WarInfoTransformer
from war_info_fetcher import WarInfoFetcher

class UpdateOrchestrator:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)

        # Initialize components
        self.api_client = Helldivers2ApiClient(max_retries=3)
        self.db_manager = DatabaseManager()

        # Initialize transformers
        self.war_status_transformer = WarStatusTransformer()
        self.planet_transformer = PlanetTransformer()
        self.news_transformer = NewsTransformer()
        self.campaign_transformer = CampaignTransformer()
        self.major_orders_transformer = MajorOrderTransformer()
        self.planet_history_transformer = PlanetHistoryTransformer()
        self.war_info_transformer = WarInfoTransformer()

        # Initialize fetchers
        self.war_status_fetcher = WarStatusFetcher(self.api_client, self.war_status_transformer, self.db_manager)
        self.planet_fetcher = PlanetFetcher(self.api_client, self.planet_transformer, self.db_manager)
        self.news_fetcher = NewsFetcher(self.api_client, self.news_transformer, self.db_manager)
        self.campaign_fetcher = CampaignFetcher(self.api_client, self.campaign_transformer, self.db_manager)
        self.major_orders_fetcher = MajorOrdersFetcher(self.api_client, self.major_orders_transformer, self.db_manager)
        self.planet_history_fetcher = PlanetHistoryFetcher(self.api_client, self.planet_history_transformer, self.db_manager)
        self.war_info_fetcher = WarInfoFetcher(self.api_client, self.db_manager)

    def run_update(self) -> bool:
        start_time = datetime.now()
        self.logger.info(f"Starting Helldivers 2 data update at {start_time}")

        results = {
            'planets': False,
            'campaign': False,
            'war_info': False,
            'war_status': False,
            'news': False,
            'major_orders': False,
            'planet_history': False
        }

        # Run fetchers in correct order
        try:
            results['planets'] = self.planet_fetcher.fetch_and_store()
        except Exception as e:
            self.logger.error(f"PlanetFetcher failed: {str(e)}")
        try:
            results['campaign'] = self.campaign_fetcher.fetch_and_store()
        except Exception as e:
            self.logger.error(f"CampaignFetcher failed: {str(e)}")
        try:
            results['war_info'] = self.war_info_fetcher.fetch_and_store()
        except Exception as e:
            self.logger.error(f"WarInfoFetcher failed: {str(e)}")
        try:
            results['war_status'] = self.war_status_fetcher.fetch_and_store()
        except Exception as e:
            self.logger.error(f"WarStatusFetcher failed: {str(e)}")
        try:
            results['news'] = self.news_fetcher.fetch_and_store()
        except Exception as e:
            self.logger.error(f"NewsFetcher failed: {str(e)}")
        try:
            results['major_orders'] = self.major_orders_fetcher.fetch_and_store()
        except Exception as e:
            self.logger.error(f"MajorOrdersFetcher failed: {str(e)}")
        try:
            results['planet_history'] = self.planet_history_fetcher.fetch_and_store()
        except Exception as e:
            self.logger.error(f"PlanetHistoryFetcher failed: {str(e)}")

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        success_count = sum(1 for result in results.values() if result)
        failure_count = len(results) - success_count

        self.logger.info(f"Update completed in {duration} seconds. Successes: {success_count}, Failures: {failure_count}")
        for name, result in results.items():
            status = "Success" if result else "Failed"
            self.logger.info(f"{name}: {status}")

        return success_count == len(results)
