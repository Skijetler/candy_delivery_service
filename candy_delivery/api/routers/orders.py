from fastapi import APIRouter, status
from fastapi_sqlalchemy import db

import candy_delivery.db.crud as crud
import candy_delivery.api.schema as schema


router = APIRouter()

@router.post("", summary="import orders", status_code=status.HTTP_201_CREATED, response_model=schema.OrdersPostResponse)
async def import_orders(orders: schema.OrdersPostRequest):
    pass

@router.post("/assign", summary="assign orders to a courier by id", status_code=status.HTTP_200_OK, response_model=schema.OrdersPostAssignResponse)
async def assign_orders(courier_id: schema.CourierId):
    pass

@router.post("/complete", summary="marks orders as completed", status_code=status.HTTP_200_OK, response_model=schema.OrderId)
async def complete_orders(completed_order: schema.OrderPostCompleteRequest):
    pass