from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from models.order_model import Order
from services.order_service import OrderService
from websocket.socket_manager import manager
from database.memory_store import chat_history
import json

router = APIRouter()

@router.post("/chat")
async def chat_endpoint(request: dict):
    """
    MAIN ENDPOINT - Handles all frontend communication
    
    Expected request body:
    {
        "type": "create_order" | "get_orders" | "update_status" | "add_timeline",
        "data": { ... }
    }
    """
    try:
        request_type = request.get("type")
        data = request.get("data", {})
        
        if request_type == "create_order":
            # Create new order
            order = Order(**data)
            OrderService.create_order(order)
            chat_history.append({
                "role": "system",
                "content": f"Order created: {order.part_name}",
                "type": request_type
            })
            return {
                "status": "success",
                "message": "Order created successfully",
                "order": order.dict()
            }
        
        elif request_type == "get_orders":
            # Retrieve all orders
            all_orders = OrderService.get_all_orders()
            return {
                "status": "success",
                "orders": all_orders
            }
        
        elif request_type == "get_order":
            # Retrieve specific order
            order_id = data.get("order_id")
            order = OrderService.get_order_by_id(order_id)
            if order:
                return {
                    "status": "success",
                    "order": order
                }
            return {
                "status": "error",
                "message": "Order not found"
            }
        
        elif request_type == "update_status":
            # Update order status
            order_id = data.get("order_id")
            status = data.get("status")
            if OrderService.update_status(order_id, status):
                OrderService.add_timeline(order_id, f"Status updated to {status}")
                chat_history.append({
                    "role": "system",
                    "content": f"Order {order_id} status updated to {status}",
                    "type": request_type
                })
                return {
                    "status": "success",
                    "message": f"Order status updated to {status}"
                }
            return {
                "status": "error",
                "message": "Order not found"
            }
        
        elif request_type == "add_timeline":
            # Add timeline event
            order_id = data.get("order_id")
            event = data.get("event")
            if OrderService.add_timeline(order_id, event):
                return {
                    "status": "success",
                    "message": "Timeline event added"
                }
            return {
                "status": "error",
                "message": "Order not found"
            }
        
        elif request_type == "get_chat_history":
            # Retrieve chat history
            return {
                "status": "success",
                "history": chat_history
            }
        
        else:
            return {
                "status": "error",
                "message": f"Unknown request type: {request_type}"
            }
    
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time communication"""
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Broadcast to all connected clients
            await manager.broadcast({
                "type": "message",
                "content": message
            })
    except WebSocketDisconnect:
        manager.disconnect(websocket)
