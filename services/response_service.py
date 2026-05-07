from datetime import datetime
from typing import Dict, Any, Optional


class ResponseGenerator:
    """
    Generate cinematic responses that match frontend animation system.
    
    VERY IMPORTANT: Every response includes ui_hint for animation triggers!
    
    Frontend uses ui_hint to trigger animations:
    - success-glow: Green success animation
    - error-pulse: Red error animation
    - pulse-info: Blue info animation
    - fade-in: Smooth fade-in
    """
    
    @staticmethod
    def _base_response(
        response_type: str,
        message: str,
        status: str = "success",
        data: Dict[str, Any] = None,
        ui_hint: str = "fade-in"
    ) -> Dict[str, Any]:
        """
        Base response format - includes everything.
        """
        return {
            "type": response_type,
            "status": status,
            "message": message,
            "data": data or {},
            "ui_hint": ui_hint,
            "timestamp": datetime.now().isoformat()
        }
    
    # ===== SUCCESS RESPONSES =====
    
    @staticmethod
    def order_created_response(order: Dict[str, Any]) -> Dict[str, Any]:
        """
        Response when order is successfully created.
        """
        return ResponseGenerator._base_response(
            response_type="ORDER_CREATED",
            message=f"✅ Manufacturing order #{order.get('id')} successfully registered.",
            data=order,
            ui_hint="success-glow"
        )
    
    @staticmethod
    def status_updated_response(
        order: Dict[str, Any],
        old_status: str,
        new_status: str
    ) -> Dict[str, Any]:
        """
        Response when order status is updated.
        """
        return ResponseGenerator._base_response(
            response_type="STATUS_UPDATED",
            message=f"Order #{order.get('id')} status: {old_status} → {new_status}",
            data=order,
            ui_hint="pulse-success"
        )
    
    @staticmethod
    def quality_logged_response(
        order: Dict[str, Any],
        quality_type: str
    ) -> Dict[str, Any]:
        """
        Response when quality check is logged.
        """
        return ResponseGenerator._base_response(
            response_type="QUALITY_LOGGED",
            message=f"✓ {quality_type} quality check logged for order #{order.get('id')}",
            data=order,
            ui_hint="pulse-info"
        )
    
    @staticmethod
    def orders_list_response(
        orders: list,
        filter_type: str = "all"
    ) -> Dict[str, Any]:
        """
        Response with list of orders.
        """
        return ResponseGenerator._base_response(
            response_type="ORDERS_LIST",
            message=f"Found {len(orders)} {filter_type} orders",
            data={
                "orders": orders,
                "count": len(orders),
                "filter": filter_type
            },
            ui_hint="fade-in"
        )
    
    @staticmethod
    def data_extracted_response(
        extracted_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Response when AI successfully extracts data.
        """
        return ResponseGenerator._base_response(
            response_type="DATA_EXTRACTED",
            message="Manufacturing requirements extracted successfully",
            data=extracted_data,
            ui_hint="success-glow"
        )
    
    # ===== ERROR RESPONSES =====
    
    @staticmethod
    def error_response(
        message: str,
        error_code: str = "ERROR",
        ui_hint: str = "error-pulse"
    ) -> Dict[str, Any]:
        """
        Generic error response.
        """
        return ResponseGenerator._base_response(
            response_type="ERROR",
            message=message,
            status="error",
            data={"error_code": error_code},
            ui_hint=ui_hint
        )
    
    @staticmethod
    def order_not_found_response(order_id: int) -> Dict[str, Any]:
        """
        Response when order is not found.
        """
        return ResponseGenerator.error_response(
            message=f"❌ Order #{order_id} not found",
            error_code="ORDER_NOT_FOUND"
        )
    
    @staticmethod
    def invalid_data_response(missing_fields: list) -> Dict[str, Any]:
        """
        Response when required data is missing.
        """
        fields_str = ", ".join(missing_fields)
        return ResponseGenerator.error_response(
            message=f"Missing required information: {fields_str}",
            error_code="INVALID_DATA"
        )
    
    @staticmethod
    def unknown_intent_response() -> Dict[str, Any]:
        """
        Response when intent cannot be determined.
        """
        return ResponseGenerator.error_response(
            message="❓ I didn't understand that. Try: 'Create order', 'Mark order as accepted', 'Show all orders'",
            error_code="UNKNOWN_INTENT",
            ui_hint="pulse-warning"
        )
    
    # ===== STREAMING RESPONSES =====
    
    @staticmethod
    def streaming_response(
        chunk: str,
        is_complete: bool = False
    ) -> Dict[str, Any]:
        """
        Response for streaming/typing effect.
        """
        return ResponseGenerator._base_response(
            response_type="STREAM_CHUNK",
            message=chunk,
            data={"is_complete": is_complete},
            ui_hint="typing" if not is_complete else "complete"
        )
    
    # ===== INFO RESPONSES =====
    
    @staticmethod
    def thinking_response() -> Dict[str, Any]:
        """
        Response while thinking/processing.
        """
        return ResponseGenerator._base_response(
            response_type="THINKING",
            message="🤔 Analyzing your request...",
            data={},
            ui_hint="pulse-thinking"
        )
    
    @staticmethod
    def success_message(message: str) -> Dict[str, Any]:
        """
        Generic success message.
        """
        return ResponseGenerator._base_response(
            response_type="SUCCESS",
            message=message,
            ui_hint="success-glow"
        )
    
    @staticmethod
    def info_message(message: str) -> Dict[str, Any]:
        """
        Generic info message.
        """
        return ResponseGenerator._base_response(
            response_type="INFO",
            message=message,
            ui_hint="fade-in"
        )
