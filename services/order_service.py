from database.memory_store import orders
from models.order_model import Order
from datetime import datetime

class OrderService:
    @staticmethod
    def create_order(order: Order):
        """Create a new order and store it"""
        orders.append(order.dict())
        return order
    
    @staticmethod
    def update_status(order_id: int, status: str):
        """Update order status"""
        for order in orders:
            if order['id'] == order_id:
                order['status'] = status
                return True
        return False
    
    @staticmethod
    def add_timeline(order_id: int, event: str):
        """Add timeline event to an order"""
        for order in orders:
            if order['id'] == order_id:
                order['timeline'].append({
                    'timestamp': datetime.now().isoformat(),
                    'event': event
                })
                return True
        return False
    
    @staticmethod
    def get_all_orders():
        """Retrieve all orders"""
        return orders
    
    @staticmethod
    def get_order_by_id(order_id: int):
        """Retrieve specific order"""
        for order in orders:
            if order['id'] == order_id:
                return order
        return None
