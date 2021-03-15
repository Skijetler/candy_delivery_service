import enum
from typing import List, ForwardRef
from pydantic import BaseModel


class CourierType(str, enum.Enum):
    foot = "foot"
    bike = "bike"
    car  = "car"

# Order
class OrderPostRequest(BaseModel):
    order_id: int
    weight: float
    region: int
    delivery_hours: List[str]

class Order(OrderPostRequest):
    assign_time: str
    completed: bool = False
    completed_time: str
    courier_id: int
    courier: 'Courier'

    class Config:
        orm_mode = True

# Courier
class CourierPostRequest(BaseModel):
    courier_id: int
    courier_type: CourierType
    regions: List[int]
    working_hours: List[str]

class CourierGetResponse(CourierPostRequest):
    rating: float
    earnings: int

class CourierPathRequest(BaseModel):
    courier_type: CourierType
    regions: List[int]
    working_hours: List[str]

class Courier(CourierGetResponse):
    orders: List[Order] = []

    class Config:
        orm_mode = True

Order.update_forward_refs()

# Lists
class CouriersPostRequest(BaseModel):
    data: List[CourierPostRequest]

class OrdersPostRequest(BaseModel):
    data: List[OrderPostRequest]