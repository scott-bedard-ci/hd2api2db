"""HTTP client wrapper for the Helldivers 2 API with retry support."""

import requests
import logging
import time

class Helldivers2ApiClient:
    """Simple wrapper exposing methods for each Helldivers API endpoint."""
    BASE_URL = 'https://helldiverstrainingmanual.com/api/v1/war'

    def __init__(self, max_retries=3, timeout=10):
        self.max_retries = max_retries
        self.timeout = timeout

    def _make_request(self, endpoint, params=None):
        url = f"{self.BASE_URL}/{endpoint}"
        retry_count = 0
        while retry_count < self.max_retries:
            try:
                response = requests.get(url, params=params, timeout=self.timeout)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                retry_count += 1
                if retry_count == self.max_retries:
                    logging.error(f"Failed to fetch {url}: {str(e)}")
                    raise
                wait_time = 2 ** retry_count
                logging.warning(f"Retrying {url} in {wait_time} seconds...")
                time.sleep(wait_time)

    def get_war_status(self):
        return self._make_request('status')

    def get_war_info(self):
        return self._make_request('info')

    def get_news(self, from_time=None):
        params = {'from': from_time} if from_time else None
        return self._make_request('news', params=params)

    def get_campaign(self):
        return self._make_request('campaign')

    def get_planet_history(self, planet_index, timeframe=None):
        endpoint = f"history/{planet_index}"
        params = {'timeframe': timeframe} if timeframe else None
        return self._make_request(endpoint, params=params)

    def get_major_orders(self):
        return self._make_request('major-orders')

    def get_planets(self):
        # This endpoint is outside the /war path
        url = 'https://helldiverstrainingmanual.com/api/v1/planets'
        retry_count = 0
        while retry_count < self.max_retries:
            try:
                response = requests.get(url, timeout=self.timeout)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                retry_count += 1
                if retry_count == self.max_retries:
                    logging.error(f"Failed to fetch {url}: {str(e)}")
                    raise
                wait_time = 2 ** retry_count
                logging.warning(f"Retrying {url} in {wait_time} seconds...")
                time.sleep(wait_time)

    def get_campaigns(self):
        return self._make_request('campaign') 