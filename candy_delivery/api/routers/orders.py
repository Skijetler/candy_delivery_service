from datetime import datetime
from fastapi import APIRouter, status
from fastapi.responses import ORJSONResponse
from fastapi_sqlalchemy import db

import candy_delivery.db.crud as crud
import candy_delivery.api.schema as schema


router = APIRouter()

@router.post("", summary="import orders", status_code=status.HTTP_201_CREATED, response_model=schema.OrdersPostResponse)
async def import_orders(orders: schema.OrdersPostRequest):
    resp = schema.OrdersPostResponse(orders=[])
    for order in orders.data:
        if (await crud.get_order(db=db.session, order_id=order.order_id)) == None:
            await crud.create_order(db=db.session, order=order)
            resp.orders.append(schema.Id(id=order.order_id))
    return resp

@router.post("/assign", summary="assign orders to a courier by id", status_code=status.HTTP_200_OK, response_model=schema.OrdersPostAssignResponse)
async def assign_orders(courier_id: schema.CourierId):
    resp = schema.OrdersPostAssignResponse(orders=[], assign_time="")
    courier_db = await crud.get_courier(db=db.session, courier_id=courier_id.courier_id)
    
    if courier_db is None:
        return ORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST)
    
    orders = await crud.get_valid_orders(db=db.session, regions=courier_db.regions, working_hours=courier_db.working_hours, max_weight=schema.get_max_weight(courier_db.courier_type))
    
    if len(orders) == 0:
        return ORJSONResponse(content=resp.dict(exclude={'assign_time'}),status_code=status.HTTP_200_OK)
    
    assign_time = datetime.utcnow()
    resp.assign_time = assign_time.isoformat() + 'Z'
    
    for order in orders:
        await crud.assign_order(db=db.session, order=order, assign_time=assign_time, courier_id=courier_db.id)
        resp.orders.append(schema.Id(id=order.id))
    
    return resp

@router.post("/complete", summary="marks orders as completed", status_code=status.HTTP_200_OK, response_model=schema.OrderId)
async def complete_order(completed_order: schema.OrderPostCompleteRequest):
    order_db = await crud.get_order(db=db.session, order_id=completed_order.order_id)
    
    if order_db == None:
        return ORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST)
    if order_db.courier_id != completed_order.courier_id or order_db.courier_id is None:
        return ORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST)
    
    courier_db = await crud.get_courier(db=db.session, courier_id=completed_order.courier_id)
    order_db = await crud.complete_order(db=db.session, order=order_db, complete_time=completed_order.complete_time)
    completed_orders = await crud.get_completed_orders(db=db.session, courier_id=completed_order.courier_id)
    
    periods = dict()
    periods[completed_orders[0].region] = [round(completed_orders[0].completed_time.timestamp()) - round(completed_orders[0].assign_time.timestamp())]
    for i, order in enumerate(completed_orders[1:]):
        if order.region not in periods.keys():
            periods[order.region] = []
        periods[order.region].append(round(order.completed_time.timestamp()) - round(completed_orders[i-1].completed_time.timestamp()))
    mean_periods = [(sum(region_periods) / len(region_periods)) for region_periods in periods.values()]
    
    rating = (60*60 - min(min(mean_periods), 60*60))/(60*60) * 5 
    earnings = 500 * schema.get_earnings_coef(courier_db.courier_type)
    await crud.update_courier_rating_and_earnings(db=db.session, courier=courier_db, rating=rating, earnings=earnings)
    
    return schema.OrderId(order_id=order_db.id)