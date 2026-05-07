# 🏗️ Nova Nexus Backend Architecture Explained

## 📋 Overview

We built a **FastAPI-based Manufacturing Order Management System** with:
- **Real-time WebSocket communication** for live updates
- **REST API** for order operations
- **In-memory storage** for quick prototyping
- **Modular design** for easy scaling

---

## 🎯 High-Level Flow

```
Frontend (React/Vue)
    ↓
POST /chat endpoint (REST API)
    ↓
Order Service (Business Logic)
    ↓
Memory Store (Database)
    ↓
Response sent back to Frontend
    ↓
WebSocket broadcasts to all clients
```

---

## 📁 Directory Structure Explained

```
nova-nexus/
├── main.py                    ← Entry point (starts FastAPI server)
├── requirements.txt           ← All dependencies listed
├── .env                       ← Configuration (PORT, DEBUG mode)
│
├── models/
│   ├── __init__.py
│   └── order_model.py        ← Defines Order structure (Pydantic)
│
├── database/
│   ├── __init__.py
│   └── memory_store.py       ← Lists for storing orders & chat history
│
├── services/
│   ├── __init__.py
│   └── order_service.py      ← Business logic (CRUD operations)
│
├── routes/
│   ├── __init__.py
│   └── chat_routes.py        ← ALL API endpoints (main hub)
│
└── websocket/
    ├── __init__.py
    └── socket_manager.py     ← Real-time connection management
```

---

## 🔧 How Each Component Works

### 1️⃣ **models/order_model.py** - Data Structure
```python
# Defines what an Order looks like
class Order(BaseModel):
    id: int
    part_name: str
    material: str
    quantity: int
    deadline: str
    status: str
    timeline: List = []
```
**Why?** Pydantic validates data automatically before it's stored.

---

### 2️⃣ **database/memory_store.py** - Storage
```python
orders = []              # Stores all orders
chat_history = []        # Stores conversation history
```
**Why?** Simple Python lists. Fast for hackathon. Can swap for database later.

---

### 3️⃣ **services/order_service.py** - Business Logic
```python
class OrderService:
    @staticmethod
    def create_order(order)     # Create new order
    @staticmethod
    def update_status()         # Change order status
    @staticmethod
    def add_timeline()          # Track order events
    @staticmethod
    def get_all_orders()        # Retrieve all orders
```
**Why?** Separates business logic from API routes. Easy to test.

---

### 4️⃣ **websocket/socket_manager.py** - Real-Time Communication
```python
class ConnectionManager:
    async def connect()         # Accept WebSocket connection
    async def disconnect()      # Remove connection
    async def broadcast()       # Send to ALL clients
    async def stream_message()  # Typing effect (char by char)
```
**Why?** Manages multiple clients. Broadcasts updates instantly.

---

### 5️⃣ **routes/chat_routes.py** - API Endpoints (Main Hub)

#### **POST /chat** (The ONLY endpoint needed)
Handles ALL operations via `type` field:

```json
{
  "type": "create_order",
  "data": {
    "id": 1,
    "part_name": "Engine Block",
    "material": "Aluminum",
    "quantity": 50,
    "deadline": "2026-05-10",
    "status": "pending"
  }
}
```

**Supported Operations:**
- `create_order` → OrderService.create_order()
- `get_orders` → OrderService.get_all_orders()
- `get_order` → OrderService.get_order_by_id()
- `update_status` → OrderService.update_status()
- `add_timeline` → OrderService.add_timeline()

#### **WS /ws** (WebSocket for Real-Time)
```javascript
// Frontend connects
const ws = new WebSocket("ws://localhost:8000/ws");

// Server broadcasts updates
ws.onmessage = (event) => {
  console.log(event.data); // Real-time order update
};
```

---

### 6️⃣ **main.py** - FastAPI Application
```python
app = FastAPI()
app.add_middleware(CORSMiddleware)  # Allow frontend requests
app.include_router(router)           # Include all routes
```

**What happens on startup:**
1. FastAPI initializes
2. CORS middleware enables frontend communication
3. Routes are registered
4. Server listens on `0.0.0.0:8000`

---

## 🚀 Data Flow Example: Create Order

```
1. FRONTEND sends POST request
   └─ POST /chat with order data

2. ROUTES catches the request
   └─ Validates JSON format

3. ORDER SERVICE processes it
   └─ OrderService.create_order(order)

4. DATABASE stores it
   └─ orders.append(order)

5. CHAT HISTORY logs it
   └─ chat_history.append(event)

6. WEBSOCKET broadcasts
   └─ manager.broadcast({"status": "order_created"})

7. FRONTEND receives via REST
   └─ {"status": "success", "order": {...}}

8. ALL CONNECTED CLIENTS get WebSocket update
   └─ Real-time UI update
```

---

## 🔄 Why This Architecture?

| Feature | Benefit |
|---------|---------|
| **Modular (separated concerns)** | Easy to understand & modify |
| **FastAPI** | Fast, modern, auto-docs at `/docs` |
| **Single /chat endpoint** | Frontend has ONE endpoint to call |
| **WebSocket** | Real-time updates without polling |
| **In-memory storage** | Fast (no database latency) |
| **Pydantic validation** | Bad requests rejected automatically |

---

## 📊 API Contract (What Frontend Needs to Know)

### Create Order
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "type": "create_order",
    "data": {
      "id": 1,
      "part_name": "Widget",
      "material": "Steel",
      "quantity": 100,
      "deadline": "2026-05-15",
      "status": "pending"
    }
  }'
```

### Get All Orders
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"type": "get_orders"}'
```

### Update Status
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "type": "update_status",
    "data": {"order_id": 1, "status": "completed"}
  }'
```

---

## 🎓 How to Explain This to Others

### **1-Minute Summary:**
> "We built a manufacturing order system using FastAPI. The frontend sends requests to a single `/chat` endpoint, which processes orders and stores them. WebSocket broadcasts real-time updates to all connected clients."

### **5-Minute Summary:**
> "Our backend has three layers:
> 1. **Routes** - API endpoints that receive requests
> 2. **Services** - Business logic that processes orders
> 3. **Database** - In-memory storage
> 
> When a frontend request comes in, it goes through the route, gets processed by the service, stored in the database, and broadcasted via WebSocket. This keeps everything synchronized."

### **10-Minute Deep Dive:**
1. Show the file structure
2. Explain each component (models → services → routes)
3. Demo a request/response cycle
4. Show WebSocket connection
5. Explain why we chose this architecture (speed, modularity, scalability)

---

## 🔗 How Frontend Connects

```javascript
// 1. Create order
fetch('http://localhost:8000/chat', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    type: 'create_order',
    data: {...}
  })
})
.then(res => res.json())
.then(data => console.log(data));

// 2. Listen for real-time updates
const ws = new WebSocket('ws://localhost:8000/ws');
ws.onmessage = (event) => {
  const update = JSON.parse(event.data);
  console.log('Real-time update:', update);
};
```

---

## ✅ Checklist: What We Built

- ✅ FastAPI application setup
- ✅ Order model with validation
- ✅ CRUD service layer
- ✅ REST API endpoint
- ✅ WebSocket real-time updates
- ✅ CORS enabled for frontend
- ✅ Environment configuration
- ✅ In-memory database
- ✅ Error handling
- ✅ Auto API documentation at `/docs`

---

## 🚀 Next Steps

1. **Frontend Development** - Build React/Vue app
2. **Test Integration** - POST to `/chat`, listen to `/ws`
3. **Add Database** - Swap memory_store for PostgreSQL/MongoDB
4. **Deploy** - Push to production (AWS/Azure/Heroku)
5. **Scale** - Add authentication, logging, monitoring

---

## 📞 Questions?

**Q: Why not use a database?**
A: For hackathon speed. Data resets on restart, which is fine for demo.

**Q: Why single `/chat` endpoint?**
A: Simpler for frontend. `type` field determines operation.

**Q: How do we deploy this?**
A: `pip install -r requirements.txt && python main.py` (or Docker)

**Q: Can multiple people use it simultaneously?**
A: Yes! WebSocket handles multiple connections via ConnectionManager.
