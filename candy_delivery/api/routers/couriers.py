from fastapi import APIRouter, status
from fastapi_sqlalchemy import db

import candy_delivery.db.crud as crud
import candy_delivery.api.schema as schema


router = APIRouter()

@router.post("", summary="import couriers", status_code=status.HTTP_201_CREATED, response_model=schema.CouriersPostResponse)
async def import_couriers(couriers: schema.CouriersPostRequest):
    pass

@router.get("/{courier_id}", summary="get courier info", status_code=status.HTTP_200_OK, response_model=schema.CourierGetResponse)
async def find_courier_by_id(courier_id: int):
    pass

@router.patch("/{courier_id}", summary="update courier by id", status_code=status.HTTP_200_OK, response_model=schema.CourierPathResponse)
async def update_courier_by_id(courier_id: int, courier_info: schema.CourierPathRequest):
    pass