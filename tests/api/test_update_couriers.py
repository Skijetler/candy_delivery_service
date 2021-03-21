import pytest
from random import randint
from datetime import datetime

from test.test_data import generate_courier_db, generate_courier
from candy_delivery.db.models import Courier, Order


@pytest.mark.asyncio
async def test_update_courier(api_client, migrated_db_session):
    courier = generate_courier_db()
    courier_update = generate_courier()

    courier_db = Courier(
        id=courier["courier_id"],
        courier_type=courier["courier_type"],
        regions=courier["regions"],
        working_hours=courier["working_hours"],
        rating=courier["rating"],
        earnings=courier["earnings"]
    )
    migrated_db_session.add(courier_db)
    migrated_db_session.commit()

    response = await api_client.patch("/couriers/" + str(courier["courier_id"]),
                                        json = {
                                            "courier_type": courier_update['courier_type'],
                                            "regions": courier_update['regions'],
                                            "working_hours": courier_update['working_hours']
                                        }
                                    )
    
    assert response.status_code == 200
    assert response.json() == {
        "courier_id": courier["courier_id"],
        "courier_type": courier_update['courier_type'],
        "regions": courier_update['regions'],
        "working_hours": courier_update['working_hours']
    }


@pytest.mark.asyncio
async def test_update_courier_not_found(api_client):
    courier_update = generate_courier()

    response = await api_client.patch("/couriers/" + str(randint(0, 100)),
                                        json = {
                                            "courier_type": courier_update['courier_type'],
                                            "regions": courier_update['regions'],
                                            "working_hours": courier_update['working_hours']
                                        }
                                    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_courier_cancel_orders(api_client, migrated_db_session):
    courier_db = Courier(
        id=6,
        courier_type="car",
        regions=[20, 15, 9, 4],
        working_hours=["09:00-16:00"],
    )
    order_db_1 = Order(
        id=1,
        weight=40,
        region=4,
        delivery_hours=["09:30-12:30"],
        assign_time=datetime.utcnow(),
        courier_id=6
    )
    order_db_2 = Order(
        id=2,
        weight=14,
        region=20,
        delivery_hours=["14:30-16:00"],
        assign_time=datetime.utcnow(),
        courier_id=6
    )
    order_db_3 = Order(
        id=3,
        weight=16,
        region=15,
        delivery_hours=["12:00-15:30"],
        assign_time=datetime.utcnow(),
        courier_id=6
    )
    order_db_4 = Order(
        id=4,
        weight=10,
        region=9,
        delivery_hours=["08:00-08:30"],
        assign_time=datetime.utcnow(),
        courier_id=6
    )

    migrated_db_session.add(courier_db)
    migrated_db_session.add(order_db_1)
    migrated_db_session.add(order_db_2)
    migrated_db_session.add(order_db_3)
    migrated_db_session.add(order_db_4)
    migrated_db_session.commit()

    response = await api_client.patch("/couriers/6",
                                        json = {
                                            "courier_type": "bike",
                                            "regions": [20, 9]
                                        }
                                     )

    assert response.status_code == 200
    assert response.json() == {
        "courier_id": 6,
        "courier_type": "bike",
        "regions": [20, 9],
        "working_hours": ["09:00-16:00"],
    }

    valid_orders_ids = [order.id for order in migrated_db_session.query(Order).filter(Order.courier_id != None)]
    assert valid_orders_ids == [2]