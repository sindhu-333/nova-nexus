from pydantic import BaseModel
from typing import List

class Order(BaseModel):
    id: int
    part_name: str
    material: str
    quantity: int
    deadline: str
    status: str
    timeline: List = []
