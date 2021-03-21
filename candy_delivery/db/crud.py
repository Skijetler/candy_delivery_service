import re
import datetime
from sqlalchemy.orm import Session
from typing import List

import candy_delivery.api.schema as schema
import candy_delivery.db.models as models

async def get_courier(db: Session, courier_id: int):
    return db.query(models.Courier).filter(models.Courier.id == courier_id).first()

async def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()

async def create_courier(db: Session, courier: schema.CourierPostRequest):
    db_courier = models.Courier(id=courier.courier_id,
                            courier_type=courier.courier_type,
                            regions=courier.regions,
                            working_hours=courier.working_hours
                            )
    db.add(db_courier)
    db.commit()
    db.refresh(db_courier)
    return db_courier

async def update_courier(db: Session, courier_id: int, courier_update_data: schema.CourierPathRequest):
    db_courier = await get_courier(db=db, courier_id=courier_id)
    if db_courier is None:
        return None
    if courier_update_data.courier_type is not None:
        db_courier.courier_type = courier_update_data.courier_type
    if courier_update_data.regions is not None:
        db_courier.regions = courier_update_data.regions
    if courier_update_data.working_hours is not None:
        db_courier.working_hours = courier_update_data.working_hours
    db.commit()
    return db_courier

async def update_courier_rating_and_earnings(db: Session, courier: models.Courier, rating: float, earnings: int):
    courier.rating = rating
    courier.earnings += earnings
    db.commit()
    return courier


time_period_regex = re.compile(r"(?P<begin_hour>(0[0-9]|1[0-9]|2[0-3])):(?P<begin_minutes>[0-5][0-9])-(?P<end_hour>(0[0-9]|1[0-9]|2[0-3])):(?P<end_minutes>[0-5][0-9])")

def check_if_in_time_period(time_period: str, in_time_period: str):
    time_period = (re.match(time_period_regex, time_period)).groupdict()
    in_time_period = (re.match(time_period_regex, in_time_period)).groupdict()
    begin_in_time_period = int(in_time_period['begin_hour']) * 60 + int(in_time_period['begin_minutes'])
    end_in_time_period = int(in_time_period['end_hour']) * 60 + int(in_time_period['end_minutes'])
    begin_time_period = int(time_period['begin_hour']) * 60 + int(time_period['begin_minutes'])
    end_time_period = int(time_period['end_hour']) * 60 + int(time_period['end_minutes'])
    if (begin_in_time_period <= begin_time_period <= end_in_time_period) or (begin_in_time_period <= end_time_period <= end_in_time_period):
        return True
    else:
        return False

def check_if_in_time_periods(time_periods: List[str], in_time_periods: List[str]):
    for in_time_range in in_time_periods:
        for time_range in time_periods:
            if check_if_in_time_period(time_range, in_time_range):
                    return True
    return False    


async def get_valid_orders(db: Session, regions: List[int], working_hours: List[str], max_weight: float):
    valid_range_orders = db.query(models.Order).filter(models.Order.region._in(regions), 
                                                       models.Order.assign_time == None,
                                                       models.Order.weight <= max_weight
                                                       )
    valid_orders = []
    for order in valid_range_orders:
        if check_if_in_time_periods(order.delivery_hours, working_hours):
            valid_orders.append(order)
                    
    return valid_orders


async def create_order(db: Session, order: schema.OrderPostRequest):
    db_order = models.Order(id=order.order_id,
                            weight=order.weight,
                            region=order.region,
                            delivery_hours=order.delivery_hours
                            )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

async def assign_order(db: Session, order: models.Order, assign_time: datetime.datetime, courier_id: int):
    order.assign_time = assign_time
    order.courier_id = courier_id
    db.commit()
    return order

async def unassign_order(db: Session, order: models.Order):
    order.assign_time = None
    order.courier_id = None
    db.commit()
    return order

async def complete_order(db: Session, order: models.Order, complete_time: datetime.datetime):
    order.completed_time = complete_time
    order.completed = True
    db.commit()
    return order

async def get_completed_orders(db: Session, courier_id: int):
    return db.query(models.Order).filter(models.Order.courier_id == courier_id, models.Order.completed == True).order_by(models.Order.completed_time)

async def get_uncompleted_orders(db: Session, courier_id: int):
    return db.query(models.Order).filter(models.Order.courier_id == courier_id, models.Order.completed == False)