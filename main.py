import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

<<<<<<< HEAD
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.chat_routes import router as chat_router
from routes.order_routes import router as order_router
=======
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routes.chat_routes import router as chat_router
from routes.order_routes import router as order_router
from app.routes.auth_routes import router as auth_router
>>>>>>> bfe028c (feat: complete Nova Nexus manufacturing OS)
import uvicorn

app = FastAPI(
    title="Nova Nexus",
    description="Manufacturing Order Management System with AI",
    version="1.0.0"
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(chat_router, prefix="/api")
app.include_router(order_router, prefix="/api")
<<<<<<< HEAD

@app.get("/")
=======
app.include_router(auth_router, prefix="/api")

# Mount static files
app.mount("/", StaticFiles(directory=".", html=True), name="static")

@app.get("/api/")
>>>>>>> bfe028c (feat: complete Nova Nexus manufacturing OS)
def home():
    return {
        "status": "Nova Nexus Running",
        "version": "1.0.0",
        "endpoints": {
            "chat": "POST /api/chat",
            "orders": "GET /api/orders",
            "websocket": "WS /ws",
            "docs": "/docs"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)