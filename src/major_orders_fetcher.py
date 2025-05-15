import logging

class MajorOrdersFetcher:
    def __init__(self, api_client, transformer, db_manager):
        self.api_client = api_client
        self.transformer = transformer
        self.db_manager = db_manager
        self.logger = logging.getLogger(__name__)

    def fetch_and_store(self):
        try:
            self.logger.info("Fetching major orders data")
            major_orders_data = self.api_client.get_major_orders()

            self.logger.info("Transforming major orders data")
            transformed_data = self.transformer.transform(major_orders_data)

            self.logger.info("Storing major orders data")
            for order in transformed_data:
                print(f"Importing major order: id32={order['id32']} type={order['order_type']}")
                self.db_manager.upsert_major_order(order)

            self.logger.info("Major orders data updated successfully")
            return True
        except Exception as e:
            self.logger.error(f"Error updating major orders data: {str(e)}")
            return False 