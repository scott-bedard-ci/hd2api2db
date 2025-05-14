from datetime import datetime

class MajorOrderTransformer:
    @staticmethod
    def transform(major_orders_data):
        """Transform raw major order data from API to database format."""
        transformed_orders = []
        for order in major_orders_data:
            transformed_item = {
                'description': order.get('description'),
                'target_planet_id': order.get('targetPlanetId'),
                'expiry_time': order.get('expiryTime', None),
                # Add other fields as needed based on your schema
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            }
            transformed_orders.append(transformed_item)
        return transformed_orders 