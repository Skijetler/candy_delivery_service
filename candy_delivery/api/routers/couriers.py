from fastapi import APIRouter
from fastapi.responses import ORJSONResponse
from fastapi_sqlalchemy import db

import candy_delivery.db.crud as crud
import candy_delivery.api.schema as schema


router = APIRouter()

@router.post("", summary="import couriers")
async def import_couriers(couriers: schema.CouriersPostRequest):
    pass

@router.get("/{courier_id}", summary="get courier info")
async def find_courier_by_id(courier_id: int):
    pass

@router.patch("/{courier_id}", summary="update courier by id")
async def update_courier_by_id(courier_id: int, courier_info: schema.Courier):
    pass