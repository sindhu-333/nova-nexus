from fastapi import APIRouter

router = APIRouter()

@router.get("/orders")
def get_orders():
    return {"status": "success", "orders": []}

@router.get("/orders/{order_id}")
def get_order(order_id: int):
    return {"status": "success", "order_id": order_id}

@router.post("/orders")
def create_order(order: dict):
    return {"status": "success", "order": order}
