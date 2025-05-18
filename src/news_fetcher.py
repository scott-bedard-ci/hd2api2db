"""Fetches news entries and persists them via the database manager."""
from __future__ import annotations
import logging
from typing import Any

class NewsFetcher:
    """Handle retrieval and storage of news via ``fetch_and_store``."""
    def __init__(self, api_client: Any, transformer: Any, db_manager: Any) -> None:

        self.api_client = api_client
        self.transformer = transformer
        self.db_manager = db_manager
        self.logger = logging.getLogger(__name__)

    def fetch_and_store(self) -> bool:
        try:
            self.logger.info("Fetching news data")
            news_data = self.api_client.get_news()

            self.logger.info("Transforming news data")
            transformed_data = self.transformer.transform(news_data)

            self.logger.info("Storing news data")
            for news in transformed_data:
                print(f"Importing news: id={news['id']} type={news['type']}")
                self.db_manager.upsert_news(news)

            self.logger.info("News data updated successfully")
            return True
        except Exception as e:
            self.logger.error(f"Error updating news data: {str(e)}")
            return False
