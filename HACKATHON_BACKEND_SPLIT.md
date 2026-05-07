# 🚀 Backend Split for 5-Hour Hackathon (2 Developers)

## ⏱️ Timeline: 5 Hours Total
- **Setup (15 min):** GitHub + local setup
- **Development (4 hours 15 min):** Parallel work
- **Integration (20 min):** Testing & fixes
- **Buffer (10 min):** Emergency fixes

---

## 🔧 PART 0: GitHub Collaboration Setup (15 mins - DO THIS FIRST)

### Step 1: Initialize Git Repository
```bash
cd c:\Users\Home\OneDrive\Desktop\nova-nexus
git init
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

### Step 2: Create GitHub Repo
1. Go to [github.com](https://github.com/new)
2. Create repo: `nova-nexus-backend`
3. Choose **PUBLIC** (hackathon)
4. Copy the HTTPS link

### Step 3: Add Remote & Initial Commit
```bash
git remote add origin https://github.com/YOUR_USERNAME/nova-nexus-backend.git
git branch -M main
git add .
git commit -m "Initial backend structure"
git push -u origin main
```

### Step 4: Create Feature Branches
```bash
# Person 1 (Infrastructure)
git checkout -b feature/infrastructure-gateway

# Person 2 (AI & Workflows)
git checkout -b feature/ai-services-workflows
```

### Step 5: Collaboration Workflow
**EVERY 30 MINUTES:**
```bash
git add .
git commit -m "Progress: [describe what you did]"
git push origin feature/YOUR_BRANCH_NAME
```

**BEFORE FINAL SUBMISSION:**
```bash
git checkout main
git pull origin main
git merge feature/infrastructure-gateway
git merge feature/ai-services-workflows
git push origin main
```

---

## 🏗️ PART 1: Core Infrastructure & Intent Engine (Person 1)
**Estimated: 2 hours 15 minutes**

### Responsibility
- WebSocket infrastructure
- Intent routing engine
- Response generation system
- Memory stores
- Real-time message handling

### Structure to Create
```
backend/
├── main.py                      (Person 1)
├── .env                         (Person 1)
├── requirements.txt             (Person 1)
├── app/
│   └── __init__.py             (Person 1)
├── websocket/
│   ├── __init__.py
│   └── socket_manager.py       (Person 1)
├── database/
│   ├── __init__.py
│   └── memory_store.py         (Person 1)
├── utils/
│   ├── __init__.py
│   ├── regex_utils.py          (Person 1)
│   └── timestamps.py           (Person 1)
└── services/
    ├── __init__.py
    ├── intent_service.py       (Person 1)
    └── response_service.py     (Person 1)
```

### Step-by-Step Implementation

#### **STEP 1.1: Project Setup (10 min)**

Create `requirements.txt`:
```
fastapi==0.104.1
uvicorn==0.24.0
python-socketio==5.9.0
python-socketio[asyncio_client]==5.9.0
python-engineio==4.8.0
python-dotenv==1.0.0
groq==0.4.1
pydantic==2.5.0
```

Create `.env`:
```
GROQ_API_KEY=your_groq_key_here
BACKEND_PORT=8000
```

Create `backend/app/__init__.py` (empty file)

#### **STEP 1.2: Memory Store (20 min)**

Create `backend/database/memory_store.py`:
```python
from datetime import datetime
from typing import List, Dict, Any

class MemoryStore:
    def __init__(self):
        # Orders storage
        self.orders: List[Dict[str, Any]] = []
        self.order_counter = 0
        
        # Chat history
        self.chat_history: List[Dict[str, Any]] = []
        
        # Connected clients (for WebSocket broadcasting)
        self.connected_clients = set()
    
    # ===== ORDER MANAGEMENT =====
    def create_order(self, order_data: Dict) -> Dict:
        """Create new order and return with ID"""
        self.order_counter += 1
        order = {
            "id": self.order_counter,
            "created_at": datetime.now().isoformat(),
            "status": "PENDING",
            "timeline": [
                {
                    "type": "CREATED",
                    "timestamp": datetime.now().isoformat(),
                    "note": "Order created"
                }
            ],
            **order_data
        }
        self.orders.append(order)
        return order
    
    def get_order(self, order_id: int) -> Dict:
        """Retrieve order by ID"""
        for order in self.orders:
            if order["id"] == order_id:
                return order
        return None
    
    def update_order_status(self, order_id: int, status: str, note: str = "") -> Dict:
        """Update order status and add to timeline"""
        order = self.get_order(order_id)
        if order:
            order["status"] = status
            order["timeline"].append({
                "type": "STATUS_UPDATE",
                "timestamp": datetime.now().isoformat(),
                "status": status,
                "note": note
            })
        return order
    
    def get_orders_by_status(self, status: str) -> List[Dict]:
        """Get all orders with specific status"""
        return [o for o in self.orders if o["status"] == status]
    
    def get_all_orders(self) -> List[Dict]:
        """Get all orders"""
        return self.orders
    
    # ===== CHAT MANAGEMENT =====
    def add_chat_message(self, role: str, content: str, metadata: Dict = None) -> Dict:
        """Add message to chat history"""
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        self.chat_history.append(message)
        return message
    
    def get_chat_history(self, limit: int = 50) -> List[Dict]:
        """Get recent chat messages"""
        return self.chat_history[-limit:]
    
    def clear_chat_history(self):
        """Clear all chat history"""
        self.chat_history = []

# Global instance
memory = MemoryStore()
```

#### **STEP 1.3: Intent Detection Service (20 min)**

Create `backend/services/intent_service.py`:
```python
import re
from enum import Enum

class IntentType(str, Enum):
    CREATE_ORDER = "CREATE_ORDER"
    UPDATE_STATUS = "UPDATE_STATUS"
    QUALITY_REPORT = "QUALITY_REPORT"
    VIEW_ORDERS = "VIEW_ORDERS"
    GET_ORDER_DETAILS = "GET_ORDER_DETAILS"
    UNKNOWN = "UNKNOWN"

class IntentService:
    @staticmethod
    def detect_intent(message: str) -> IntentType:
        """
        Detect user intent from message using regex + keyword matching.
        FAST and CHEAP - no LLM needed here.
        """
        message_lower = message.lower()
        
        # CREATE_ORDER: mentions quantity, material, deadline
        if any(keyword in message_lower for keyword in [
            "need ", "order ", "require ", "deliver ", "produce "
        ]):
            if any(word in message_lower for word in [
                "by ", "deadline ", "friday", "monday", "tuesday", "wednesday", 
                "thursday", "saturday", "sunday", "january", "february", "march",
                "april", "may", "june", "july", "august", "september", "october",
                "november", "december", "qty", "quantity", "units"
            ]):
                return IntentType.CREATE_ORDER
        
        # UPDATE_STATUS: marked as, status, accepted, rejected, in-progress
        if any(keyword in message_lower for keyword in [
            "mark ", "status ", "accepted", "rejected", "in-progress", 
            "completed", "update order", "change status", "set as"
        ]):
            if any(word in message_lower for word in ["order", "it", "this"]):
                return IntentType.UPDATE_STATUS
        
        # QUALITY_REPORT: inspection, quality, test, pass, fail, thermal, tensile
        if any(keyword in message_lower for keyword in [
            "inspection", "quality", "test", "pass", "fail", "passed", 
            "failed", "thermal", "tensile", "pressure", "dimension", "verified"
        ]):
            return IntentType.QUALITY_REPORT
        
        # VIEW_ORDERS: show, list, get, view all, orders status
        if any(keyword in message_lower for keyword in [
            "show ", "list ", "get all", "view ", "fetch ", "display "
        ]):
            if "order" in message_lower:
                return IntentType.VIEW_ORDERS
        
        # GET_ORDER_DETAILS: show order, details, info
        if any(keyword in message_lower for keyword in [
            "order ", "details", "info", "show", "get"
        ]):
            # Check if specific order number mentioned
            if re.search(r'order\s+\d+|#\d+|\d+', message_lower):
                return IntentType.GET_ORDER_DETAILS
        
        return IntentType.UNKNOWN
    
    @staticmethod
    def extract_keywords(message: str) -> Dict[str, Any]:
        """Extract useful keywords from message"""
        import re
        
        keywords = {
            "materials": [],
            "quantities": [],
            "dates": [],
            "statuses": [],
            "order_ids": []
        }
        
        # Extract numbers for quantities and order IDs
        numbers = re.findall(r'\d+', message)
        keywords["quantities"] = [int(n) for n in numbers if 10 <= int(n) <= 10000]
        keywords["order_ids"] = [int(n) for n in numbers if 1 <= int(n) <= 9]
        
        # Extract materials
        materials = [
            "steel", "titanium", "aluminum", "copper", "brass",
            "iron", "nickel", "zinc", "platinum", "gold"
        ]
        for material in materials:
            if material in message.lower():
                keywords["materials"].append(material.capitalize())
        
        # Extract date patterns
        date_keywords = [
            "monday", "tuesday", "wednesday", "thursday", "friday",
            "saturday", "sunday", "january", "february", "march", "april",
            "may", "june", "july", "august", "september", "october",
            "november", "december"
        ]
        for date_kw in date_keywords:
            if date_kw in message.lower():
                keywords["dates"].append(date_kw.capitalize())
        
        # Extract statuses
        statuses = ["accepted", "rejected", "pending", "completed", "in-progress"]
        for status in statuses:
            if status in message.lower():
                keywords["statuses"].append(status.upper())
        
        return keywords
```

Fix the import:
```python
from typing import Dict, Any
```

#### **STEP 1.4: Response Generation Service (20 min)**

Create `backend/services/response_service.py`:
```python
from typing import Dict, Any, Optional

class ResponseGenerator:
    """
    Generate cinematic responses that match frontend animation system.
    Every response includes ui_hint for animation triggers.
    """
    
    @staticmethod
    def success_response(
        response_type: str,
        message: str,
        data: Dict[str, Any] = None,
        ui_hint: str = "success-glow"
    ) -> Dict[str, Any]:
        """Generate successful response with animation hint"""
        return {
            "type": response_type,
            "status": "success",
            "message": message,
            "data": data or {},
            "ui_hint": ui_hint,
            "timestamp": __import__("datetime").datetime.now().isoformat()
        }
    
    @staticmethod
    def error_response(
        message: str,
        error_code: str = "ERROR",
        ui_hint: str = "error-pulse"
    ) -> Dict[str, Any]:
        """Generate error response"""
        return {
            "type": "ERROR",
            "status": "error",
            "message": message,
            "error_code": error_code,
            "data": {},
            "ui_hint": ui_hint,
            "timestamp": __import__("datetime").datetime.now().isoformat()
        }
    
    @staticmethod
    def streaming_response(
        chunk: str,
        is_complete: bool = False
    ) -> Dict[str, Any]:
        """For streaming AI responses"""
        return {
            "type": "STREAM_CHUNK",
            "chunk": chunk,
            "is_complete": is_complete,
            "timestamp": __import__("datetime").datetime.now().isoformat()
        }
    
    # ===== SPECIFIC RESPONSE BUILDERS =====
    
    @staticmethod
    def order_created_response(order: Dict) -> Dict[str, Any]:
        return ResponseGenerator.success_response(
            response_type="ORDER_CREATED",
            message=f"Manufacturing order #{order['id']} successfully registered.",
            data=order,
            ui_hint="success-glow"
        )
    
    @staticmethod
    def status_updated_response(order: Dict, old_status: str, new_status: str) -> Dict[str, Any]:
        return ResponseGenerator.success_response(
            response_type="STATUS_UPDATED",
            message=f"Order #{order['id']} status updated: {old_status} → {new_status}",
            data=order,
            ui_hint="pulse-success"
        )
    
    @staticmethod
    def quality_logged_response(order: Dict, quality_type: str) -> Dict[str, Any]:
        return ResponseGenerator.success_response(
            response_type="QUALITY_UPDATE",
            message=f"{quality_type} logged for order #{order['id']}",
            data=order,
            ui_hint="pulse-info"
        )
    
    @staticmethod
    def orders_list_response(orders: list, filter_type: str = "all") -> Dict[str, Any]:
        return ResponseGenerator.success_response(
            response_type="ORDERS_LIST",
            message=f"Retrieved {len(orders)} {filter_type} orders",
            data={"orders": orders, "count": len(orders)},
            ui_hint="fade-in"
        )
    
    @staticmethod
    def ai_extraction_response(extracted_data: Dict) -> Dict[str, Any]:
        return ResponseGenerator.success_response(
            response_type="DATA_EXTRACTED",
            message="Manufacturing requirements extracted",
            data=extracted_data,
            ui_hint="success-glow"
        )
```

#### **STEP 1.5: Regex Utilities (15 min)**

Create `backend/utils/regex_utils.py`:
```python
import re

class RegexUtils:
    @staticmethod
    def extract_order_id(text: str) -> int:
        """Extract order ID from text like 'order 3' or '#3'"""
        match = re.search(r'order\s+(\d+)|#(\d+)', text.lower())
        if match:
            return int(match.group(1) or match.group(2))
        return None
    
    @staticmethod
    def extract_quantity(text: str) -> int:
        """Extract quantity from text"""
        # Look for patterns like "200 steel brackets" or "qty: 200"
        match = re.search(r'(?:qty|quantity|need|order|require)?\s*(\d+)\s*(?:units|pieces|items)?', text.lower())
        if match:
            num = int(match.group(1))
            # Reasonable manufacturing quantities: 1-10000
            if 1 <= num <= 10000:
                return num
        return None
    
    @staticmethod
    def extract_material(text: str) -> str:
        """Extract material name"""
        materials = {
            'steel': r'\bsteel\b',
            'titanium': r'\btitanium\b',
            'aluminum': r'\b(?:aluminum|aluminium)\b',
            'copper': r'\bcopper\b',
            'brass': r'\bbrass\b',
            'iron': r'\biron\b',
            'nickel': r'\bnickel\b',
            'zinc': r'\bzinc\b'
        }
        text_lower = text.lower()
        for material, pattern in materials.items():
            if re.search(pattern, text_lower):
                return material.capitalize()
        return None
    
    @staticmethod
    def extract_deadline(text: str) -> str:
        """Extract deadline from text"""
        # Simple extraction - just find dates mentioned
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        months = ['january', 'february', 'march', 'april', 'may', 'june', 
                  'july', 'august', 'september', 'october', 'november', 'december']
        
        text_lower = text.lower()
        
        for day in days:
            if day in text_lower:
                return day.capitalize()
        
        for month in months:
            if month in text_lower:
                # Try to find date like "July 20"
                match = re.search(rf'{month}\s+(\d+)', text_lower, re.IGNORECASE)
                if match:
                    return f"{month.capitalize()} {match.group(1)}"
                return month.capitalize()
        
        return None
```

#### **STEP 1.6: Timestamps Utility (10 min)**

Create `backend/utils/timestamps.py`:
```python
from datetime import datetime

class TimestampUtils:
    @staticmethod
    def get_iso_now() -> str:
        """Get current timestamp in ISO format"""
        return datetime.now().isoformat()
    
    @staticmethod
    def get_unix_now() -> int:
        """Get current timestamp in Unix format"""
        return int(datetime.now().timestamp())
    
    @staticmethod
    def format_timestamp(timestamp_str: str) -> str:
        """Format ISO timestamp to readable format"""
        try:
            dt = datetime.fromisoformat(timestamp_str)
            return dt.strftime("%B %d, %Y at %H:%M:%S")
        except:
            return timestamp_str
```

#### **STEP 1.7: WebSocket Manager (25 min)**

Create `backend/websocket/socket_manager.py`:
```python
import json
from typing import Set, Dict, Any

class ConnectionManager:
    """Manage WebSocket connections for real-time communication"""
    
    def __init__(self):
        self.active_connections: Set = set()
        self.client_metadata: Dict[str, Any] = {}
    
    async def connect(self, websocket, client_id: str):
        """Register new WebSocket connection"""
        await websocket.accept()
        self.active_connections.add(websocket)
        self.client_metadata[client_id] = {
            "connected_at": __import__("datetime").datetime.now().isoformat(),
            "messages_sent": 0
        }
        print(f"✅ Client {client_id} connected. Total: {len(self.active_connections)}")
    
    def disconnect(self, websocket, client_id: str):
        """Unregister WebSocket connection"""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            if client_id in self.client_metadata:
                del self.client_metadata[client_id]
        print(f"❌ Client {client_id} disconnected. Total: {len(self.active_connections)}")
    
    async def broadcast(self, message: Dict[str, Any]):
        """Send message to all connected clients"""
        message_json = json.dumps(message)
        for connection in self.active_connections:
            try:
                await connection.send_text(message_json)
            except Exception as e:
                print(f"⚠️ Broadcast error: {e}")
    
    async def send_personal(self, websocket, message: Dict[str, Any]):
        """Send message to specific client"""
        try:
            await websocket.send_text(json.dumps(message))
        except Exception as e:
            print(f"⚠️ Send error: {e}")
    
    def get_connection_count(self) -> int:
        """Get number of active connections"""
        return len(self.active_connections)

# Global instance
manager = ConnectionManager()
```

#### **STEP 1.8: Main FastAPI App (30 min)**

Create `backend/main.py`:
```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import os
import json
from dotenv import load_dotenv
import uuid

# Load environment variables
load_dotenv()

# Import our modules
from database.memory_store import memory
from services.intent_service import IntentService, IntentType
from services.response_service import ResponseGenerator
from websocket.socket_manager import manager
from utils.regex_utils import RegexUtils

# Create FastAPI app
app = FastAPI(
    title="Nova Nexus - Manufacturing Operations AI",
    description="Real-time conversational manufacturing order system",
    version="1.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== HEALTH CHECK =====
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "orders": len(memory.get_all_orders()),
        "connections": manager.get_connection_count()
    }

# ===== WebSocket ENDPOINT (Main conversational gateway) =====
@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    """
    Main WebSocket endpoint for real-time conversational interaction.
    This is the ONLY entry point the frontend needs.
    """
    client_id = str(uuid.uuid4())[:8]
    await manager.connect(websocket, client_id)
    
    try:
        while True:
            # Receive message from frontend
            data = await websocket.receive_text()
            user_message = json.loads(data)["message"]
            
            print(f"📨 [{client_id}] {user_message}")
            
            # Add to chat history
            memory.add_chat_message("user", user_message)
            
            # STEP 1: Detect Intent (FAST - no LLM)
            intent = IntentService.detect_intent(user_message)
            print(f"🎯 Intent detected: {intent}")
            
            # Send to frontend: "thinking" state
            await manager.send_personal(
                websocket,
                ResponseGenerator.streaming_response(
                    chunk="Analyzing your request...",
                    is_complete=False
                )
            )
            
            # STEP 2: Route based on intent
            response = None
            
            if intent == IntentType.CREATE_ORDER:
                # Will be handled by Person 2 (AI extraction)
                # For now, send placeholder
                response = ResponseGenerator.error_response(
                    "ORDER_SERVICE_NOT_READY",
                    message="Order service initializing..."
                )
            
            elif intent == IntentType.UPDATE_STATUS:
                order_id = RegexUtils.extract_order_id(user_message)
                if order_id:
                    order = memory.get_order(order_id)
                    if order:
                        # Extract new status from message
                        new_status = "ACCEPTED" if "accepted" in user_message.lower() else "PENDING"
                        old_status = order["status"]
                        updated_order = memory.update_order_status(order_id, new_status, user_message)
                        response = ResponseGenerator.status_updated_response(
                            updated_order, old_status, new_status
                        )
                    else:
                        response = ResponseGenerator.error_response(f"Order #{order_id} not found")
                else:
                    response = ResponseGenerator.error_response("Could not identify order number")
            
            elif intent == IntentType.QUALITY_REPORT:
                # Will be handled by Person 2
                response = ResponseGenerator.error_response(
                    "QUALITY_SERVICE_NOT_READY",
                    message="Quality service initializing..."
                )
            
            elif intent == IntentType.VIEW_ORDERS:
                orders = memory.get_all_orders()
                response = ResponseGenerator.orders_list_response(orders)
            
            elif intent == IntentType.GET_ORDER_DETAILS:
                order_id = RegexUtils.extract_order_id(user_message)
                if order_id:
                    order = memory.get_order(order_id)
                    if order:
                        response = ResponseGenerator.success_response(
                            response_type="ORDER_DETAILS",
                            message=f"Order #{order_id} details",
                            data=order
                        )
                    else:
                        response = ResponseGenerator.error_response(f"Order #{order_id} not found")
                else:
                    response = ResponseGenerator.error_response("Could not identify order number")
            
            else:
                response = ResponseGenerator.error_response(
                    "Could not understand your request. Try: 'Create order', 'Mark order X as accepted', 'Show all orders'"
                )
            
            # Send response
            if response:
                memory.add_chat_message("assistant", response.get("message", ""))
                await manager.send_personal(websocket, response)
                print(f"📤 Response sent: {response['type']}")
            
            # Broadcast to all clients for live updates
            await manager.broadcast({
                "type": "SYSTEM_UPDATE",
                "total_orders": len(memory.get_all_orders()),
                "active_clients": manager.get_connection_count()
            })
    
    except WebSocketDisconnect:
        manager.disconnect(websocket, client_id)
    except Exception as e:
        print(f"❌ WebSocket Error: {e}")
        manager.disconnect(websocket, client_id)

# ===== REST ENDPOINTS (Secondary - for testing) =====

@app.get("/orders")
async def get_orders(status: str = None):
    """Get all orders, optionally filtered by status"""
    if status:
        orders = memory.get_orders_by_status(status.upper())
    else:
        orders = memory.get_all_orders()
    
    return ResponseGenerator.orders_list_response(orders, filter_type=status or "all")

@app.get("/orders/{order_id}")
async def get_order(order_id: int):
    """Get specific order details"""
    order = memory.get_order(order_id)
    if order:
        return ResponseGenerator.success_response(
            response_type="ORDER_DETAILS",
            message=f"Order #{order_id} details",
            data=order
        )
    return ResponseGenerator.error_response(f"Order #{order_id} not found")

@app.get("/chat-history")
async def get_chat_history(limit: int = 50):
    """Get chat history"""
    history = memory.get_chat_history(limit)
    return ResponseGenerator.success_response(
        response_type="CHAT_HISTORY",
        message="Chat history retrieved",
        data={"messages": history, "count": len(history)}
    )

# ===== STARTUP =====
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("BACKEND_PORT", 8000))
    print(f"""
    🚀 Nova Nexus Backend Starting...
    
    ✅ WebSocket: ws://localhost:{port}/ws/chat
    ✅ REST API: http://localhost:{port}
    ✅ Docs: http://localhost:{port}/docs
    """)
    
    uvicorn.run(app, host="0.0.0.0", port=port)
```

Create `backend/__init__.py` (empty):
```python
```

---

## 🤖 PART 2: AI Services & Workflow Engine (Person 2)
**Estimated: 2 hours 15 minutes**

### Responsibility
- Groq AI integration for data extraction
- Order service (create orders with AI extraction)
- Quality service (quality timeline tracking)
- Chat routes (conversational endpoints)
- Order routes (order CRUD endpoints)

### Structure to Create
```
backend/
├── routes/
│   ├── __init__.py
│   ├── chat_routes.py          (Person 2)
│   └── order_routes.py         (Person 2)
├── services/
│   ├── __init__.py
│   ├── ai_service.py           (Person 2)
│   ├── order_service.py        (Person 2)
│   └── quality_service.py      (Person 2)
├── models/
│   ├── __init__.py
│   ├── order_model.py          (Person 2)
│   └── chat_model.py           (Person 2)
```

### Step-by-Step Implementation

#### **STEP 2.1: AI Service (Groq Integration) (30 min)**

Create `backend/services/ai_service.py`:
```python
import os
import json
from groq import Groq

class AIService:
    """
    AI service using Groq for structured data extraction.
    IMPORTANT: Only use for extraction, NOT for every response.
    Keeps token costs minimal and judges will love this.
    """
    
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "mixtral-8x7b-32768"
    
    def extract_order_data(self, user_message: str) -> Dict[str, Any]:
        """
        Extract structured manufacturing data from natural language.
        Uses JSON-only prompt for efficiency.
        """
        extraction_prompt = f"""Extract manufacturing order data from this message and return ONLY valid JSON:

Message: "{user_message}"

Return this exact JSON structure (no markdown, no explanation):
{{
    "part_name": "extracted part name or null",
    "material": "extracted material or null",
    "quantity": integer quantity or null,
    "deadline": "extracted deadline or null",
    "specifications": ["any specs mentioned"],
    "success": true
}}

If no valid order data, set "success": false and return nulls."""
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=200,  # Very small for extraction
                messages=[
                    {"role": "user", "content": extraction_prompt}
                ]
            )
            
            response_text = response.content[0].text.strip()
            
            # Try to parse JSON
            try:
                data = json.loads(response_text)
                return data
            except json.JSONDecodeError:
                # Try to extract JSON from response
                start = response_text.find('{')
                end = response_text.rfind('}') + 1
                if start != -1 and end > start:
                    data = json.loads(response_text[start:end])
                    return data
                return {"success": False, "error": "Could not parse response"}
        
        except Exception as e:
            print(f"❌ AI Service Error: {e}")
            return {"success": False, "error": str(e)}
    
    def extract_quality_type(self, message: str) -> str:
        """Extract quality check type from message"""
        prompt = f"""What type of quality check is mentioned? Return exactly one word:

Message: "{message}"

Options: THERMAL, TENSILE, DIMENSION, PRESSURE, INSPECTION, VERIFICATION, OTHER

Reply with ONLY the word."""
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=10,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text.strip().upper()
        except:
            return "INSPECTION"

# Global instance
ai_service = AIService()
```

Add required import:
```python
from typing import Dict, Any
```

#### **STEP 2.2: Order Model (15 min)**

Create `backend/models/order_model.py`:
```python
from pydantic import BaseModel
from typing import Optional, List

class OrderCreate(BaseModel):
    """Model for creating orders"""
    part_name: str
    material: str
    quantity: int
    deadline: Optional[str] = None
    specifications: Optional[List[str]] = None

class OrderUpdate(BaseModel):
    """Model for updating order status"""
    status: str
    note: Optional[str] = None

class OrderResponse(BaseModel):
    """Model for order response"""
    id: int
    part_name: str
    material: str
    quantity: int
    status: str
    created_at: str
    deadline: Optional[str] = None
```

#### **STEP 2.3: Chat Model (10 min)**

Create `backend/models/chat_model.py`:
```python
from pydantic import BaseModel
from typing import Optional, Dict, Any

class ChatMessage(BaseModel):
    """Model for chat messages"""
    message: str
    metadata: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    """Model for chat response"""
    type: str
    status: str
    message: str
    data: Dict[str, Any]
    ui_hint: str
```

#### **STEP 2.4: Order Service (30 min)**

Create `backend/services/order_service.py`:
```python
from typing import Dict, Any, Optional
from database.memory_store import memory
from services.ai_service import ai_service

class OrderService:
    """
    Handle order creation, extraction, and processing.
    This is where AI extraction happens.
    """
    
    @staticmethod
    def create_order_from_message(user_message: str) -> Dict[str, Any]:
        """
        Create order from natural language using AI extraction.
        
        Returns: {
            "success": bool,
            "order": order_dict,
            "message": str
        }
        """
        # Step 1: Extract structured data using AI
        extracted = ai_service.extract_order_data(user_message)
        
        if not extracted.get("success"):
            return {
                "success": False,
                "order": None,
                "message": "Could not extract order data from your message",
                "error": extracted.get("error")
            }
        
        # Step 2: Validate extracted data
        part_name = extracted.get("part_name")
        material = extracted.get("material")
        quantity = extracted.get("quantity")
        deadline = extracted.get("deadline")
        specs = extracted.get("specifications", [])
        
        if not all([part_name, material, quantity]):
            return {
                "success": False,
                "order": None,
                "message": "Missing required order information (part, material, quantity)"
            }
        
        # Step 3: Create order in memory
        order_data = {
            "part_name": part_name,
            "material": material,
            "quantity": quantity,
            "deadline": deadline or "Not specified",
            "specifications": specs,
            "status": "PENDING"
        }
        
        order = memory.create_order(order_data)
        
        return {
            "success": True,
            "order": order,
            "message": f"Order created: {quantity} {part_name}s in {material}"
        }
    
    @staticmethod
    def get_order(order_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve order by ID"""
        return memory.get_order(order_id)
    
    @staticmethod
    def get_all_orders() -> list:
        """Get all orders"""
        return memory.get_all_orders()
    
    @staticmethod
    def get_orders_by_status(status: str) -> list:
        """Get orders filtered by status"""
        return memory.get_orders_by_status(status.upper())
    
    @staticmethod
    def update_order_status(order_id: int, new_status: str, note: str = "") -> Optional[Dict]:
        """Update order status"""
        return memory.update_order_status(order_id, new_status.upper(), note)
```

#### **STEP 2.5: Quality Service (25 min)**

Create `backend/services/quality_service.py`:
```python
from typing import Dict, Any, Optional
from datetime import datetime
from database.memory_store import memory
from services.ai_service import ai_service

class QualityService:
    """
    Handle quality checks and timeline tracking.
    This creates the impressive quality timeline that judges love.
    """
    
    @staticmethod
    def log_quality_check(order_id: int, message: str) -> Dict[str, Any]:
        """
        Log a quality check for an order.
        
        Returns: {
            "success": bool,
            "order": updated_order,
            "quality_type": str
        }
        """
        # Get order
        order = memory.get_order(order_id)
        if not order:
            return {
                "success": False,
                "order": None,
                "message": f"Order #{order_id} not found"
            }
        
        # Extract quality type using AI
        quality_type = ai_service.extract_quality_type(message)
        
        # Add to timeline
        order["timeline"].append({
            "type": "QUALITY_CHECK",
            "subtype": quality_type,
            "timestamp": datetime.now().isoformat(),
            "note": message,
            "status": "PASSED"  # Could extract pass/fail from message
        })
        
        return {
            "success": True,
            "order": order,
            "quality_type": quality_type,
            "message": f"{quality_type} check logged for order #{order_id}"
        }
    
    @staticmethod
    def get_order_timeline(order_id: int) -> Optional[Dict]:
        """Get order timeline for visualization"""
        order = memory.get_order(order_id)
        if not order:
            return None
        
        return {
            "order_id": order_id,
            "part_name": order.get("part_name"),
            "timeline": order.get("timeline", []),
            "current_status": order.get("status")
        }
    
    @staticmethod
    def get_quality_summary(order_id: int) -> Dict[str, Any]:
        """Get summary of all quality checks for an order"""
        order = memory.get_order(order_id)
        if not order:
            return {"success": False}
        
        quality_checks = [
            e for e in order.get("timeline", [])
            if e.get("type") == "QUALITY_CHECK"
        ]
        
        return {
            "success": True,
            "order_id": order_id,
            "total_checks": len(quality_checks),
            "checks": quality_checks,
            "last_check": quality_checks[-1] if quality_checks else None
        }
```

#### **STEP 2.6: Chat Routes (20 min)**

Create `backend/routes/chat_routes.py`:
```python
from fastapi import APIRouter
from models.chat_model import ChatMessage, ChatResponse
from services.response_service import ResponseGenerator
from database.memory_store import memory

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/message", response_model=ChatResponse)
async def send_chat_message(chat_msg: ChatMessage):
    """
    Send a chat message (REST alternative to WebSocket).
    Useful for testing.
    """
    user_message = chat_msg.message
    
    # Add to history
    memory.add_chat_message("user", user_message)
    
    # For REST, return simple response
    response = ResponseGenerator.success_response(
        response_type="MESSAGE_RECEIVED",
        message=f"Message received: {user_message[:50]}...",
        data={"message": user_message},
        ui_hint="fade-in"
    )
    
    memory.add_chat_message("assistant", response["message"])
    return response

@router.get("/history")
async def get_chat_history(limit: int = 50):
    """Get chat message history"""
    history = memory.get_chat_history(limit)
    return ResponseGenerator.success_response(
        response_type="CHAT_HISTORY",
        message=f"Retrieved {len(history)} messages",
        data={"messages": history},
        ui_hint="fade-in"
    )

@router.delete("/history")
async def clear_chat_history():
    """Clear all chat history"""
    memory.clear_chat_history()
    return ResponseGenerator.success_response(
        response_type="HISTORY_CLEARED",
        message="Chat history cleared",
        ui_hint="success-glow"
    )
```

#### **STEP 2.7: Order Routes (25 min)**

Create `backend/routes/order_routes.py`:
```python
from fastapi import APIRouter
from models.order_model import OrderCreate, OrderUpdate
from services.order_service import OrderService
from services.quality_service import QualityService
from services.response_service import ResponseGenerator
from database.memory_store import memory

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/create")
async def create_order(order: OrderCreate):
    """
    Create order from structured data (REST).
    WebSocket users interact through /ws/chat which handles this.
    """
    order_data = {
        "part_name": order.part_name,
        "material": order.material,
        "quantity": order.quantity,
        "deadline": order.deadline,
        "specifications": order.specifications or [],
        "status": "PENDING"
    }
    
    created_order = memory.create_order(order_data)
    
    return ResponseGenerator.success_response(
        response_type="ORDER_CREATED",
        message=f"Order #{created_order['id']} created: {order.quantity} {order.part_name}s",
        data=created_order,
        ui_hint="success-glow"
    )

@router.get("/")
async def list_orders(status: str = None):
    """List all orders, optionally filtered by status"""
    if status:
        orders = OrderService.get_orders_by_status(status)
        filter_text = f"{status} orders"
    else:
        orders = OrderService.get_all_orders()
        filter_text = "all orders"
    
    return ResponseGenerator.orders_list_response(orders, filter_text)

@router.get("/{order_id}")
async def get_order(order_id: int):
    """Get specific order details"""
    order = OrderService.get_order(order_id)
    
    if not order:
        return ResponseGenerator.error_response(f"Order #{order_id} not found")
    
    return ResponseGenerator.success_response(
        response_type="ORDER_DETAILS",
        message=f"Order #{order_id} details",
        data=order,
        ui_hint="fade-in"
    )

@router.put("/{order_id}/status")
async def update_order_status(order_id: int, update: OrderUpdate):
    """Update order status"""
    order = OrderService.get_order(order_id)
    
    if not order:
        return ResponseGenerator.error_response(f"Order #{order_id} not found")
    
    old_status = order["status"]
    updated = OrderService.update_order_status(order_id, update.status, update.note)
    
    return ResponseGenerator.status_updated_response(updated, old_status, update.status)

@router.post("/{order_id}/quality")
async def log_quality_check(order_id: int, check_data: dict):
    """Log quality check for order"""
    result = QualityService.log_quality_check(order_id, check_data.get("note", ""))
    
    if not result["success"]:
        return ResponseGenerator.error_response(result.get("message", "Failed to log quality check"))
    
    return ResponseGenerator.quality_logged_response(
        result["order"],
        result.get("quality_type", "INSPECTION")
    )

@router.get("/{order_id}/timeline")
async def get_order_timeline(order_id: int):
    """Get order event timeline"""
    timeline = QualityService.get_order_timeline(order_id)
    
    if not timeline:
        return ResponseGenerator.error_response(f"Order #{order_id} not found")
    
    return ResponseGenerator.success_response(
        response_type="ORDER_TIMELINE",
        message=f"Timeline for order #{order_id}",
        data=timeline,
        ui_hint="fade-in"
    )

@router.get("/{order_id}/quality-summary")
async def get_quality_summary(order_id: int):
    """Get quality check summary"""
    summary = QualityService.get_quality_summary(order_id)
    
    if not summary.get("success"):
        return ResponseGenerator.error_response(f"Order #{order_id} not found")
    
    return ResponseGenerator.success_response(
        response_type="QUALITY_SUMMARY",
        message=f"Quality summary for order #{order_id}",
        data=summary,
        ui_hint="fade-in"
    )
```

#### **STEP 2.8: Integrate Routes into Main (10 min)**

Person 2 needs to update `backend/main.py` to include the new routes. Add these imports and lines:

```python
# Add at top with other imports
from routes.chat_routes import router as chat_router
from routes.order_routes import router as order_router

# Add after CORSMiddleware setup, before health check
app.include_router(chat_router)
app.include_router(order_router)
```

---

## ✅ Integration Checklist (20 mins)

Both people work together on this:

```
□ Person 1: Push feature/infrastructure-gateway
  git add .
  git commit -m "feat: core infrastructure, websocket, intent detection"
  git push origin feature/infrastructure-gateway

□ Person 2: Push feature/ai-services-workflows
  git add .
  git commit -m "feat: AI services, order/quality workflows, routes"
  git push origin feature/ai-services-workflows

□ Person 1: Create Pull Request on GitHub
  - Go to repo → Pull requests
  - Create PR from feature/infrastructure-gateway → main
  - Request review from Person 2

□ Person 2: Create Pull Request on GitHub
  - Create PR from feature/ai-services-workflows → main
  - Request review from Person 1

□ Person 1: Review Person 2's changes (5 min)
  - Check for any conflicts
  - Approve PR

□ Person 2: Review Person 1's changes (5 min)
  - Approve PR

□ Merge both PRs into main
  - Merge feature/infrastructure-gateway
  - Merge feature/ai-services-workflows

□ Pull latest main locally
  git checkout main
  git pull origin main

□ Set up environment
  python -m venv venv
  source venv/Scripts/activate  # Windows
  pip install -r requirements.txt

□ Test the backend
  python backend/main.py
  # Server should start on http://localhost:8000

□ Test endpoints
  - GET http://localhost:8000/health
  - WebSocket ws://localhost:8000/ws/chat
  - GET http://localhost:8000/orders

□ Create final commit
  git add .
  git commit -m "feat: complete backend - ready for integration"
  git push origin main

□ Deploy/Share
  - Copy backend folder to your demo environment
  - Ensure .env has valid GROQ_API_KEY
```

---

## 🧪 Quick Testing Commands

**While developing locally:**

```bash
# Test REST endpoints
curl http://localhost:8000/health

# Create test order via REST
curl -X POST http://localhost:8000/orders/create \
  -H "Content-Type: application/json" \
  -d '{
    "part_name": "Steel Bracket",
    "material": "Steel",
    "quantity": 100,
    "deadline": "Friday"
  }'

# Get all orders
curl http://localhost:8000/orders

# Get order timeline
curl http://localhost:8000/orders/1/timeline
```

**Frontend WebSocket connection:**
```javascript
const socket = new WebSocket('ws://localhost:8000/ws/chat');

socket.onopen = () => {
  socket.send(JSON.stringify({
    message: "Create order for 200 titanium flanges by July 20"
  }));
};

socket.onmessage = (event) => {
  console.log(JSON.parse(event.data));
};
```

---

## 🎯 Success Criteria

**Your backend is WINNING if:**

✅ WebSocket real-time communication works  
✅ Intent detection routes to correct handler (no LLM for this)  
✅ AI extraction creates structured orders  
✅ Quality timeline builds beautifully  
✅ Responses include `ui_hint` for frontend animations  
✅ All code is pushed to GitHub with clear commit history  
✅ No database complexity (pure in-memory)  
✅ Token efficiency showcased (minimal AI calls)  

---

## 📱 Frontend Integration Points

Your frontend needs to:

1. **Connect to WebSocket:**
   ```javascript
   const socket = new WebSocket('ws://localhost:8000/ws/chat');
   ```

2. **Send messages:**
   ```javascript
   socket.send(JSON.stringify({ message: "user message" }));
   ```

3. **Listen for responses:**
   ```javascript
   socket.onmessage = (event) => {
     const response = JSON.parse(event.data);
     // Use response.ui_hint to trigger animations
     // Use response.data for UI updates
   };
   ```

4. **Response structure:**
   ```json
   {
     "type": "ORDER_CREATED",
     "status": "success",
     "message": "Manufacturing order #1 successfully registered.",
     "data": { ...order details... },
     "ui_hint": "success-glow",
     "timestamp": "2024-01-15T10:30:00"
   }
   ```

---

## 🚨 Common Pitfalls (Avoid These!)

❌ **DON'T** wait for Person 1/2 to finish before starting  
✅ **DO** work in parallel on separate branches

❌ **DON'T** use real database  
✅ **DO** use in-memory store (saves time)

❌ **DON'T** over-engineer AI prompts  
✅ **DO** use simple JSON extraction prompts

❌ **DON'T** commit broken code  
✅ **DO** test locally first

❌ **DON'T** forget ui_hint in responses  
✅ **DO** include ui_hint for every response type

❌ **DON'T** handle everything in one endpoint  
✅ **DO** separate intent detection from action

---

## 💾 Final Submission

```bash
# Before Demo:
git checkout main
git pull origin main
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
python backend/main.py

# Share with judges:
- GitHub URL
- Backend running on localhost:8000
- WebSocket ws://localhost:8000/ws/chat
```

---

**GO BUILD! 🚀 You have everything. Execute in parallel. 5 hours is plenty.**
