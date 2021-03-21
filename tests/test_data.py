from typing import List, Any, Dict
from random import randint, choice

from candy_delivery.api.schema import CourierType

def generate_courier(
                     courier_id: int = None,
                     courier_type: CourierType = None,
                     regions: List[int] = None,
                     working_hours: List[str] = None
                    ):
    
    
    if courier_id is None:
        courier_id = randint(1, 1000000)

    if courier_type is None:
        courier_type = choice(["foot", "bike", "car"])

    if regions is None:
        regions = [randint(1, 85) for _ in range(5)]

    if working_hours is None:
        working_hours = choice([["09:00-12:00", "17:00-21:00"],
                                ["14:20-15:30", "20:00-21:30"],
                                ["10:40-13:20", "16:10-19:40"]])

    return {
            'courier_id': courier_id,
            'courier_type': courier_type,
            'regions': regions,
            'working_hours': working_hours
            }

def generate_courier_db(
                     courier_id: int = None,
                     courier_type: CourierType = None,
                     regions: List[int] = None,
                     working_hours: List[str] = None,
                     rating: float = None,
                     earnings: int = None
                    ):
    
    
    if courier_id is None:
        courier_id = randint(1, 1000000)

    if courier_type is None:
        courier_type = choice(["foot", "bike", "car"])

    if regions is None:
        regions = [randint(1, 85) for _ in range(5)]

    if working_hours is None:
        working_hours = choice([["09:00-12:00", "17:00-21:00"],
                                ["14:20-15:30", "20:00-21:30"],
                                ["10:40-13:20", "16:10-19:40"]])
    
    if rating is None:
        rating = randint(0, 100)

    if earnings is None:
        earnings = randint(0, 100000)

    return {
            'courier_id': courier_id,
            'courier_type': courier_type,
            'regions': regions,
            'working_hours': working_hours,
            'rating': rating,
            'earnings': earnings
            }


def generate_order(
                    order_id: int = None,
                    weight: float = None,
                    region: int = None,
                    delivery_hours: List[str] = None
                  ):
    
    if order_id is None:
        order_id = randint(1, 1000000)

    if weight is None:
        weight = randint(1, 5000) / 100

    if region is None:
        region = randint(1, 85)

    if delivery_hours is None:
        delivery_hours = choice([["10:30-13:45", "15:00-18:00"],
                                 ["14:20-16:10", "18:30-21:40"],
                                 ["09:00-16:40", "18:50-22:10"]])

    return {
            'order_id': order_id,
            'weight': weight,
            'region': region,
            'delivery_hours': delivery_hours
            }