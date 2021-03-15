from fastapi import APIRouter
from fastapi.responses import ORJSONResponse
from fastapi_sqlalchemy import db

import candy_delivery.db.crud as crud
import candy_delivery.api.schema as schema


router = APIRouter()

@router.post("", summary="import orders")
async def import_orders(orders: schema.OrdersPostRequest):
    pass

@router.post("/assign", summary="assign orders to a courier by id")
async def assign_orders(courier_id: int):
    pass

@router.post("/complete", summary="marks orders as completed")
async def complete_orders(courier_id: int, order_id: int, complete_time: str):
    pass