from datetime import datetime
import logging
import json

class NewsTransformer:
    @staticmethod
    def transform(news_data):
        """Transform raw news data from API to database format."""
        logger = logging.getLogger(__name__)
        transformed_news = []
        for news_item in news_data:
            try:
                # Convert published from int (seconds since epoch) to MySQL DATETIME string
                published_raw = news_item['published']
                if isinstance(published_raw, int):
                    published_dt = datetime.utcfromtimestamp(published_raw)
                    published = published_dt.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    published = str(published_raw)
                transformed_item = {
                    'id': news_item['id'],
                    'published': published,
                    'type': str(news_item['type']),
                    'tagIds': json.dumps(news_item.get('tagIds', [])),
                    'message': news_item['message'],
                    'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                }
                transformed_news.append(transformed_item)
            except KeyError as e:
                logger.warning(f'Missing expected field in news item: {e}')
        return transformed_news 