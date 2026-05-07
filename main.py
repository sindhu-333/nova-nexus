from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.chat_routes import router
import uvicorn

app = FastAPI(
    title="Nova Nexus",
    description="Manufacturing Order Management System",
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
app.include_router(router)

@app.get("/")
def home():
    return {
        "status": "Nova Nexus Running",
        "version": "1.0.0",
        "endpoints": {
            "chat": "POST /chat",
            "websocket": "WS /ws",
            "docs": "/docs"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
