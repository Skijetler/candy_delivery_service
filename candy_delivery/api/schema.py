import enum
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, constr, Extra, Field, PositiveInt


TimeIntervalRegex = constr(regex=r'^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]-(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$')


def get_max_weight(courier_type: str):
    if courier_type == "foot":
        return 10
    elif courier_type == "bike":
        return 15
    else:
        return 50

def get_earnings_coef(courier_type: str):
    if courier_type == "foot":
        return 2
    elif courier_type == "bike":
        return 5
    else:
        return 9

class CourierType(str, enum.Enum):
    foot = "foot"
    bike = "bike"
    car  = "car"

class Id(BaseModel):
    id: int

# Order
class OrderId(BaseModel, extra=Extra.forbid):
    order_id: int

class OrderPostRequest(BaseModel, extra=Extra.forbid):
    order_id: int
    weight: float = Field(..., ge=0.01, le=50)
    region: PositiveInt
    delivery_hours: List[TimeIntervalRegex]

class OrderPostCompleteRequest(BaseModel, extra=Extra.forbid):
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
class CourierId(BaseModel, extra=Extra.forbid):
    courier_id: int

class CourierPostRequest(BaseModel, extra=Extra.forbid):
    courier_id: int
    courier_type: CourierType
    regions: List[PositiveInt]
    working_hours: List[TimeIntervalRegex]

class CourierGetResponse(CourierPostRequest):
    rating: Optional[float]
    earnings: int

class CourierPathRequest(BaseModel, extra=Extra.forbid):
    courier_type: Optional[CourierType]
    regions: Optional[List[PositiveInt]]
    working_hours: Optional[List[TimeIntervalRegex]]

class CourierPathResponse(BaseModel):
    courier_id: int
    courier_type: CourierType
    regions: List[PositiveInt]
    working_hours: List[TimeIntervalRegex]

class Courier(CourierGetResponse):
    orders: List[Order] = []

    class Config:
        orm_mode = True

Order.update_forward_refs()


# Lists
class CouriersPostRequest(BaseModel, extra=Extra.forbid):
    data: List[CourierPostRequest]

class OrdersPostRequest(BaseModel, extra=Extra.forbid):
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
    assign_time: str