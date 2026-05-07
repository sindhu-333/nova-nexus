from fastapi import APIRouter, HTTPException
from services.order_service import OrderService
from services.response_service import ResponseGenerator
from models.order_model import Order

router = APIRouter()

@router.get("/orders")
def get_orders():
    """Get all orders"""
    try:
        orders = OrderService.get_all_orders()
        return ResponseGenerator.orders_list_response(orders)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/orders/{order_id}")
def get_order(order_id: int):
    """Get specific order by ID"""
    try:
        order = OrderService.get_order_by_id(order_id)
        if order:
            return ResponseGenerator.order_details_response(order)
        else:
            raise HTTPException(status_code=404, detail="Order not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/orders")
def create_order(order_data: dict):
    """Create new order (alternative to chat endpoint)"""
    try:
        order = Order(**order_data)
        OrderService.create_order(order)
        OrderService.add_timeline(order.id, "Order created via API")
        return ResponseGenerator.order_created_response(order.dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/orders/{order_id}/status")
def update_order_status(order_id: int, status_data: dict):
    """Update order status"""
    try:
        new_status = status_data.get("status")
        if not new_status:
            raise HTTPException(status_code=400, detail="Status required")

        if OrderService.update_status(order_id, new_status):
            OrderService.add_timeline(order_id, f"Status updated to {new_status}")
            return ResponseGenerator.status_updated_response(order_id, new_status)
        else:
            raise HTTPException(status_code=404, detail="Order not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))