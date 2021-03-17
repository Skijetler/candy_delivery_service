import enum
from typing import List, ForwardRef
from datetime import datetime
from pydantic import BaseModel


class CourierType(str, enum.Enum):
    foot = "foot"
    bike = "bike"
    car  = "car"

class Id(BaseModel):
    id: int

# Order
class OrderId(BaseModel):
    order_id: int

class OrderPostRequest(BaseModel):
    order_id: int
    weight: float
    region: int
    delivery_hours: List[str]

class OrderPostCompleteRequest(BaseModel):
    courier_id: int 
    order_id: int 
    complete_time: datetime

class Order(OrderPostRequest):
    assign_time: datetime
    completed: bool = False
    completed_time: datetime
    courier_id: int
    courier: 'Courier'

    class Config:
        orm_mode = True

# Courier
class CourierId(BaseModel):
    courier_id: int

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

class CourierPathResponse(BaseModel):
    courier_id: int
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

class CouriersPostResponse(BaseModel):
    couriers: List[Id]

class CouriersPostValidationErrorResponse(BaseModel):
    validation_error: CouriersPostResponse

class OrdersPostResponse(BaseModel):
    orders: List[Id]

class OrdersPostValidationErrorResponse(BaseModel):
    validation_error: OrdersPostResponse

class OrdersPostAssignResponse(OrdersPostResponse):
    assign_time: datetime