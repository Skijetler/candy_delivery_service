from fastapi import APIRouter, status
from fastapi.responses import ORJSONResponse
from fastapi_sqlalchemy import db

import candy_delivery.db.crud as crud
import candy_delivery.api.schema as schema


router = APIRouter()

@router.post("", summary="import couriers", status_code=status.HTTP_201_CREATED, response_model=schema.CouriersPostResponse)
async def import_couriers(couriers: schema.CouriersPostRequest):
    resp = schema.CouriersPostResponse(couriers=[])
    for courier in couriers.data:
        if (await crud.get_courier(db=db.session, courier_id=courier.courier_id)) == None:
            await crud.create_courier(db=db.session, courier=courier)
            resp.couriers.append(schema.Id(id=courier.courier_id))
    return resp

@router.get("/{courier_id}", summary="get courier info", status_code=status.HTTP_200_OK, response_model=schema.CourierGetResponse)
async def find_courier_by_id(courier_id: int):
    courier_db = await crud.get_courier(db=db.session, courier_id=courier_id)
    if courier_db is None:
        return ORJSONResponse(status_code=status.HTTP_404_NOT_FOUND)
    resp = schema.CourierGetResponse(
        courier_id = courier_db.id,
        courier_type = courier_db.courier_type,
        regions = courier_db.regions,
        working_hours = courier_db.working_hours,
        rating = courier_db.rating,
        earnings = courier_db.earnings
    )
    return ORJSONResponse(content=resp.dict(exclude={} if resp.rating !=0 else {'rating'}), status_code=status.HTTP_200_OK)

@router.patch("/{courier_id}", summary="update courier by id", status_code=status.HTTP_200_OK, response_model=schema.CourierPathResponse)
async def update_courier_by_id(courier_id: int, courier_info: schema.CourierPathRequest):
    db_courier = await crud.update_courier(db=db.session, courier_id=courier_id, courier_update_data=courier_info)
    if db_courier is None:
        return ORJSONResponse(status_code=status.HTTP_404_NOT_FOUND)

    uncompleted_orders = await crud.get_uncompleted_orders(db=db.session, courier_id=courier_id)
    for order in uncompleted_orders:
        weight_fail  = order.weight > schema.get_max_weight(db_courier.courier_type)
        regions_fail = not (order.region in db_courier.regions)
        working_hours_fail = not (crud.check_if_in_time_periods(order.delivery_hours, db_courier.working_hours))
        if weight_fail or regions_fail or working_hours_fail:
            await crud.unassign_order(db=db.session, order=order)
    
    resp = schema.CourierPathResponse(
        courier_id = courier_id,
        courier_type = db_courier.courier_type,
        regions = db_courier.regions,
        working_hours = db_courier.working_hours
    )
    return resp