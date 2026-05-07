from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from models.order_model import Order
from services.order_service import OrderService
from services.ai_service import AIService
from services.intent_service import IntentService, IntentType
from services.response_service import ResponseGenerator
from websocket.socket_manager import manager
from database.memory_store import chat_history
from utils.regex_utils import RegexUtils
import json

router = APIRouter()

# Initialize services
ai_service = AIService()
intent_service = IntentService()
response_generator = ResponseGenerator()

@router.post("/chat")
async def chat_endpoint(request: dict):
    """
    MAIN ENDPOINT - Handles all frontend communication with AI integration

    Expected request body:
    {
        "message": "user message",
        "user_id": "optional user identifier"
    }
    """
    try:
        message = request.get("message", "").strip()
        user_id = request.get("user_id", "anonymous")

        if not message:
            return response_generator.error_response("Empty message received")

        # Store user message in chat history
        chat_history.append({
            "role": "user",
            "content": message,
            "user_id": user_id,
            "timestamp": RegexUtils.get_current_timestamp()
        })

        # 1. Detect intent using regex (fast, cheap)
        intent = intent_service.detect_intent(message)

        # 2. Route based on intent
        if intent == IntentType.CREATE_ORDER:
            return await _handle_create_order(message, user_id)

        elif intent == IntentType.UPDATE_STATUS:
            return await _handle_update_status(message, user_id)

        elif intent == IntentType.QUALITY_REPORT:
            return await _handle_quality_report(message, user_id)

        elif intent == IntentType.SHOW_ACCEPTED:
            return await _handle_show_accepted(message, user_id)

        else:
            # Unknown intent - provide helpful response
            return response_generator.unknown_intent_response(message)

    except Exception as e:
        return response_generator.error_response(str(e))

async def _handle_create_order(message: str, user_id: str):
    """Handle order creation with AI data extraction"""
    try:
        # Use AI to extract structured data from natural language
        extracted_data = ai_service.extract_order_data(message)

        if not extracted_data.get("success", False):
            return response_generator.insufficient_data_response()

        # Validate required fields
        required_fields = ["part_name", "material", "quantity", "deadline"]
        if not all(extracted_data.get(field) for field in required_fields):
            return response_generator.missing_fields_response(
                [field for field in required_fields if not extracted_data.get(field)]
            )

        # Create order using extracted data
        order_data = {
            "id": len(OrderService.get_all_orders()) + 1,
            "part_name": extracted_data["part_name"],
            "material": extracted_data["material"],
            "quantity": extracted_data["quantity"],
            "deadline": extracted_data["deadline"],
            "status": "pending",
            "timeline": []
        }

        order = Order(**order_data)
        OrderService.create_order(order)

        # Add to timeline
        OrderService.add_timeline(order.id, "Order created via AI chat")

        # Store AI response in chat history
        chat_history.append({
            "role": "assistant",
            "content": f"Order created: {order.part_name}",
            "intent": "CREATE_ORDER",
            "user_id": user_id,
            "timestamp": RegexUtils.get_current_timestamp()
        })

        return response_generator.order_created_response(order.dict())

    except Exception as e:
        return response_generator.error_response(f"Failed to create order: {str(e)}")

async def _handle_update_status(message: str, user_id: str):
    """Handle order status updates"""
    try:
        # Extract order ID and status using regex
        order_id = RegexUtils.extract_order_id(message)
        new_status = RegexUtils.extract_status(message)

        if not order_id or not new_status:
            return response_generator.missing_order_info_response()

        if OrderService.update_status(order_id, new_status):
            OrderService.add_timeline(order_id, f"Status updated to {new_status}")

            chat_history.append({
                "role": "assistant",
                "content": f"Order {order_id} status updated to {new_status}",
                "intent": "UPDATE_STATUS",
                "user_id": user_id,
                "timestamp": RegexUtils.get_current_timestamp()
            })

            return response_generator.status_updated_response(order_id, new_status)
        else:
            return response_generator.order_not_found_response(order_id)

    except Exception as e:
        return response_generator.error_response(f"Failed to update status: {str(e)}")

async def _handle_quality_report(message: str, user_id: str):
    """Handle quality report submissions"""
    try:
        order_id = RegexUtils.extract_order_id(message)
        quality_data = RegexUtils.extract_quality_data(message)

        if not order_id:
            return response_generator.missing_order_info_response()

        # Add quality report to timeline
        OrderService.add_timeline(order_id, f"Quality report: {quality_data}")

        chat_history.append({
            "role": "assistant",
            "content": f"Quality report recorded for order {order_id}",
            "intent": "QUALITY_REPORT",
            "user_id": user_id,
            "timestamp": RegexUtils.get_current_timestamp()
        })

        return response_generator.quality_report_response(order_id)

    except Exception as e:
        return response_generator.error_response(f"Failed to process quality report: {str(e)}")

async def _handle_show_accepted(message: str, user_id: str):
    """Show accepted orders"""
    try:
        all_orders = OrderService.get_all_orders()
        accepted_orders = [order for order in all_orders if order.get("status") == "accepted"]

        chat_history.append({
            "role": "assistant",
            "content": f"Showing {len(accepted_orders)} accepted orders",
            "intent": "SHOW_ACCEPTED",
            "user_id": user_id,
            "timestamp": RegexUtils.get_current_timestamp()
        })

        return response_generator.accepted_orders_response(accepted_orders)

    except Exception as e:
        return response_generator.error_response(f"Failed to retrieve orders: {str(e)}")

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