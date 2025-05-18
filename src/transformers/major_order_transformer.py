"""Transforms major order API data for ingestion."""
from __future__ import annotations
from datetime import datetime, timedelta
import json
from typing import Any, Dict, List

class MajorOrderTransformer:
    @staticmethod
    def transform(major_orders_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Transform raw major order data from API to database format."""
        transformed_orders = []
        now = datetime.now()
        for order in major_orders_data:
            expires_in = order.get('expiresIn')
            expiry_time = None
            if expires_in is not None:
                expiry_time = (now + timedelta(seconds=expires_in)).strftime('%Y-%m-%d %H:%M:%S')
            setting = order.get('setting', {})
            transformed_item = {
                'id32': order.get('id32'),
                'expires_in': expires_in,
                'expiry_time': expiry_time,
                'progress': json.dumps(order.get('progress')) if order.get('progress') is not None else None,
                'flags': setting.get('flags'),
                'override_brief': setting.get('overrideBrief'),
                'override_title': setting.get('overrideTitle'),
                'reward': json.dumps(setting.get('reward')) if setting.get('reward') is not None else None,
                'rewards': json.dumps(setting.get('rewards')) if setting.get('rewards') is not None else None,
                'task_description': setting.get('taskDescription'),
                'tasks': json.dumps(setting.get('tasks')) if setting.get('tasks') is not None else None,
                'order_type': setting.get('type'),
                'created_at': now.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': now.strftime('%Y-%m-%d %H:%M:%S'),
            }
            transformed_orders.append(transformed_item)
        return transformed_orders
