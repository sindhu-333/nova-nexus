import re
from enum import Enum
from typing import Dict, Any

class IntentType(str, Enum):
    """Intent types for routing"""
    CREATE_ORDER = "CREATE_ORDER"
    UPDATE_STATUS = "UPDATE_STATUS"
    QUALITY_REPORT = "QUALITY_REPORT"
    SHOW_ACCEPTED = "SHOW_ACCEPTED"
    UNKNOWN = "UNKNOWN"


class IntentService:
    """
    Intelligent intent detection using regex and keyword matching.
    FAST. CHEAP. NO LLM NEEDED.
    
    This is the secret to token efficiency - route before calling AI!
    """
    
    @staticmethod
    def detect_intent(message: str) -> IntentType:
        """
        Detect user intent from message using regex + keywords.
        
        Returns: IntentType enum
        """
        
        message_lower = message.lower()
        
        # ===== CREATE_ORDER =====
        # Detect: "need", "order", "require" + deadline/qty indicators
        if any(keyword in message_lower for keyword in [
            "need ", "order ", "require ", "deliver ", "produce ", "want "
        ]):
            # Verify it has deadline or quantity indicators
            if any(indicator in message_lower for indicator in [
                "by ", "friday", "monday", "tuesday", "wednesday", "thursday",
                "qty", "quantity", "units", "pieces", "pieces", "bracket", 
                "flange", "shaft", "plate"
            ]):
                return IntentType.CREATE_ORDER
        
        # ===== UPDATE_STATUS =====
        # Detect: "mark", "status", "accepted", "rejected"
        if any(keyword in message_lower for keyword in [
            "mark ", "update ", "set ", "change ", "status "
        ]):
            if "order" in message_lower or re.search(r'#\d+|order\s+\d+', message_lower):
                return IntentType.UPDATE_STATUS

        # ===== SHOW_ACCEPTED =====
        # Detect: "show", "list", "all", "accepted"
        if any(keyword in message_lower for keyword in [
            "show ", "list ", "get all", "view ", "display ", "all orders"
        ]):
            if "order" in message_lower or "accepted" in message_lower:
                return IntentType.SHOW_ACCEPTED
        
        # ===== QUALITY_REPORT =====
        # Detect: "inspection", "quality", "test", "pass", "fail"
        if any(keyword in message_lower for keyword in [
            "inspection", "quality", "test", "pass", "fail", "passed", 
            "failed", "thermal", "tensile", "pressure", "dimension", 
            "verified", "checked", "inspect"
        ]):
            return IntentType.QUALITY_REPORT
        
        return IntentType.UNKNOWN
    
    @staticmethod
    def extract_order_id(message: str) -> int:
        """
        Extract order ID from message.
        Looks for patterns like "order 3", "#3"
        
        Returns: order_id or None
        """
        
        # Look for "order X" or "#X"
        match = re.search(r'order\s+(\d+)|#(\d+)', message.lower())
        if match:
            return int(match.group(1) or match.group(2))
        return None
    
    @staticmethod
    def extract_status_from_message(message: str) -> str:
        """
        Extract new status from message.
        
        Returns: "ACCEPTED", "REJECTED", "PENDING", "IN_PROGRESS", "COMPLETED" or None
        """
        
        message_lower = message.lower()
        
        status_map = {
            "accepted": "ACCEPTED",
            "reject": "REJECTED",
            "pending": "PENDING",
            "in-progress": "IN_PROGRESS",
            "in progress": "IN_PROGRESS",
            "completed": "COMPLETED",
            "done": "COMPLETED"
        }
        
        for keyword, status in status_map.items():
            if keyword in message_lower:
                return status
        
        return None
    
    @staticmethod
    def get_intent_metadata(message: str) -> Dict[str, Any]:
        """
        Extract additional metadata from message.
        
        Returns:
        {
            "intent": IntentType,
            "order_id": int or None,
            "status": str or None,
            "needs_ai": bool
        }
        """
        
        intent = IntentService.detect_intent(message)
        
        return {
            "intent": intent,
            "order_id": IntentService.extract_order_id(message),
            "status": IntentService.extract_status_from_message(message),
            "needs_ai": intent in [IntentType.CREATE_ORDER, IntentType.QUALITY_REPORT]
        }
