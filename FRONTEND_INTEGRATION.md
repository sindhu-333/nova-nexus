# 🎯 Frontend Integration Guide

## Quick Start: Connect Your Frontend to Backend

### 1. Test Backend is Running
```bash
curl http://localhost:8000/
# Should return: {"status":"Nova Nexus Running",...}
```

### 2. Auto-Generated API Docs
Open your browser: `http://localhost:8000/docs`
- See all endpoints
- Test requests live
- View response format

---

## 🔌 JavaScript/React Examples

### Install Axios (for REST calls)
```bash
npm install axios
```

### Create Orders
```javascript
import axios from 'axios';

const createOrder = async () => {
  const response = await axios.post('http://localhost:8000/chat', {
    type: 'create_order',
    data: {
      id: 1,
      part_name: 'Engine Block',
      material: 'Aluminum',
      quantity: 50,
      deadline: '2026-05-10',
      status: 'pending'
    }
  });
  console.log(response.data);
};
```

### Retrieve All Orders
```javascript
const getOrders = async () => {
  const response = await axios.post('http://localhost:8000/chat', {
    type: 'get_orders'
  });
  console.log(response.data.orders);
};
```

### Update Order Status
```javascript
const updateOrderStatus = async (orderId, newStatus) => {
  const response = await axios.post('http://localhost:8000/chat', {
    type: 'update_status',
    data: {
      order_id: orderId,
      status: newStatus
    }
  });
  console.log(response.data);
};
```

### Add Timeline Event
```javascript
const addTimeline = async (orderId, event) => {
  const response = await axios.post('http://localhost:8000/chat', {
    type: 'add_timeline',
    data: {
      order_id: orderId,
      event: event
    }
  });
  console.log(response.data);
};
```

---

## 🔴 WebSocket for Real-Time Updates

### Connect to WebSocket
```javascript
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onopen = () => {
  console.log('Connected to real-time updates');
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Real-time update:', data);
  // Update UI here
};

ws.onerror = (error) => {
  console.error('WebSocket error:', error);
};

ws.onclose = () => {
  console.log('Disconnected from real-time updates');
};
```

### Send Message via WebSocket
```javascript
const sendMessage = (message) => {
  if (ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify(message));
  }
};
```

---

## 📱 React Component Example

```javascript
import React, { useState, useEffect } from 'react';
import axios from 'axios';

function OrderManager() {
  const [orders, setOrders] = useState([]);
  const [ws, setWs] = useState(null);

  // Connect to WebSocket on mount
  useEffect(() => {
    const websocket = new WebSocket('ws://localhost:8000/ws');
    
    websocket.onmessage = (event) => {
      console.log('Update received:', event.data);
      // Refresh orders when update comes
      fetchOrders();
    };

    setWs(websocket);

    return () => websocket.close();
  }, []);

  // Fetch orders from REST API
  const fetchOrders = async () => {
    try {
      const response = await axios.post('http://localhost:8000/chat', {
        type: 'get_orders'
      });
      setOrders(response.data.orders);
    } catch (error) {
      console.error('Error fetching orders:', error);
    }
  };

  // Create new order
  const handleCreateOrder = async (orderData) => {
    try {
      await axios.post('http://localhost:8000/chat', {
        type: 'create_order',
        data: orderData
      });
      fetchOrders(); // Refresh
    } catch (error) {
      console.error('Error creating order:', error);
    }
  };

  // Render orders
  return (
    <div>
      <h1>Orders</h1>
      {orders.map((order) => (
        <div key={order.id} style={{ border: '1px solid #ccc', padding: '10px', margin: '10px 0' }}>
          <h3>{order.part_name}</h3>
          <p>Status: {order.status}</p>
          <p>Qty: {order.quantity}</p>
          <p>Material: {order.material}</p>
        </div>
      ))}
    </div>
  );
}

export default OrderManager;
```

---

## 🐍 Python Client Example

```python
import requests
import websockets
import asyncio
import json

# REST API client
class OrderClient:
    def __init__(self, base_url='http://localhost:8000'):
        self.base_url = base_url
    
    def create_order(self, order_data):
        response = requests.post(
            f'{self.base_url}/chat',
            json={
                'type': 'create_order',
                'data': order_data
            }
        )
        return response.json()
    
    def get_orders(self):
        response = requests.post(
            f'{self.base_url}/chat',
            json={'type': 'get_orders'}
        )
        return response.json()

# WebSocket client
async def websocket_client():
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as websocket:
        while True:
            data = await websocket.recv()
            print(f"Received: {data}")

# Usage
if __name__ == '__main__':
    # REST calls
    client = OrderClient()
    
    # Create order
    new_order = client.create_order({
        'id': 1,
        'part_name': 'Widget',
        'material': 'Steel',
        'quantity': 100,
        'deadline': '2026-05-15',
        'status': 'pending'
    })
    print(new_order)
    
    # Get all orders
    orders = client.get_orders()
    print(orders)
    
    # WebSocket listener (runs in background)
    # asyncio.run(websocket_client())
```

---

## 📊 API Response Examples

### Create Order Response
```json
{
  "status": "success",
  "message": "Order created successfully",
  "order": {
    "id": 1,
    "part_name": "Engine Block",
    "material": "Aluminum",
    "quantity": 50,
    "deadline": "2026-05-10",
    "status": "pending",
    "timeline": []
  }
}
```

### Get Orders Response
```json
{
  "status": "success",
  "orders": [
    {
      "id": 1,
      "part_name": "Engine Block",
      "material": "Aluminum",
      "quantity": 50,
      "deadline": "2026-05-10",
      "status": "pending",
      "timeline": [
        {
          "timestamp": "2026-05-07T10:30:00.123456",
          "event": "Order created"
        },
        {
          "timestamp": "2026-05-07T10:35:00.123456",
          "event": "Status updated to in_progress"
        }
      ]
    }
  ]
}
```

### Error Response
```json
{
  "status": "error",
  "message": "Order not found"
}
```

---

## 🧪 Test All Endpoints

### Using cURL (Terminal)
```bash
# Test server health
curl http://localhost:8000/health

# Create order
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

# Get all orders
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"type": "get_orders"}'
```

### Using Postman
1. Create new POST request
2. URL: `http://localhost:8000/chat`
3. Body (JSON):
```json
{
  "type": "create_order",
  "data": {
    "id": 1,
    "part_name": "Widget",
    "material": "Steel",
    "quantity": 100,
    "deadline": "2026-05-15",
    "status": "pending"
  }
}
```

---

## ⚙️ Environment & Configuration

### Backend .env
```
ENVIRONMENT=development
DEBUG=True
API_HOST=0.0.0.0
API_PORT=8000
```

### Frontend Environment
For React with CRA:
```javascript
// .env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_WS_URL=ws://localhost:8000
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| **CORS error** | Backend has CORS middleware enabled. If error persists, check browser console |
| **WebSocket connection refused** | Make sure server is running: `python main.py` |
| **404 error on `/chat`** | Ensure you're using POST, not GET |
| **Order not found** | Check order ID matches stored orders |

---

## 📞 Backend Running?

```bash
# Check if server is running
curl http://localhost:8000/

# View API docs
# Open browser: http://localhost:8000/docs

# Check health
curl http://localhost:8000/health
```

---

## 🚀 Ready to Build Frontend!

You now have everything you need. Start building your React/Vue/Angular UI and connect it to these endpoints.

**Key Points:**
- Base URL: `http://localhost:8000`
- Main endpoint: `POST /chat`
- WebSocket: `ws://localhost:8000/ws`
- Auto-docs: `http://localhost:8000/docs`
