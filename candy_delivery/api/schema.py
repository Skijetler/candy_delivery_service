import enum
from typing import List, ForwardRef
from pydantic import BaseModel


class CourierType(str, enum.Enum):
    foot = "foot"
    bike = "bike"
    car  = "car"

Courier_rel = ForwardRef("Courier")

class Order(BaseModel):
    id: int
    weight: float
    region: int
    delivery_hours: List[str]
    assign_time: str
    completed: bool = False
    completed_time: str
    courier_id: int
    courier: Courier_rel

    class Config:
        orm_mode = True

class Courier(BaseModel):
    id: int
    courier_type: CourierType
    regions: List[int]
    working_hours: List[str]
    rating: float = 0
    earnings: int = 0
    occupied: bool = False
    orders: List[Order] = []

    class Config:
        orm_mode = True