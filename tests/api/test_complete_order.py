import pytest
from datetime import datetime

from candy_delivery.db.models import Courier, Order


@pytest.mark.asyncio
async def test_complete_order(api_client, migrated_db_session):
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
        assign_time=datetime.strptime("2021-01-10T09:32:14.42Z", "%Y-%m-%dT%H:%M:%S.%fZ"),
        courier_id=6
    )
    migrated_db_session.add(courier_db)
    migrated_db_session.add(order_db_1)
    migrated_db_session.commit()

    response = await api_client.post("/orders/complete",
                                        json={
                                            "courier_id": 6,
                                            "order_id": 1,
                                            "complete_time": "2021-01-10T10:00:01.42Z"
                                        })
    assert response.status_code == 200
    assert response.json() == {
        "order_id": 1
    }

    order = migrated_db_session.query(Order).filter(Order.id == order_db_1.id).first()
    assert order.completed == True

    courier = migrated_db_session.query(Courier).filter(Courier.id == courier_db.id).first()
    assert courier.rating != 0
    assert courier.earnings == 4500

@pytest.mark.asyncio
async def test_complete_order_courier_not_found(api_client, migrated_db_session):
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
        assign_time=datetime.strptime("2021-01-10T09:32:14.42Z", "%Y-%m-%dT%H:%M:%S.%fZ"),
        courier_id=6
    )
    migrated_db_session.add(courier_db)
    migrated_db_session.add(order_db_1)
    migrated_db_session.commit()

    response = await api_client.post("/orders/complete",
                                        json={
                                            "courier_id": 1,
                                            "order_id": 1,
                                            "complete_time": "2021-01-10T10:33:01.42Z"
                                        })
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_complete_order_courier_bad_order(api_client, migrated_db_session):
    courier_db_1 = Courier(
        id=6,
        courier_type="car",
        regions=[20, 15, 9, 4],
        working_hours=["09:00-16:00"],
    )
    courier_db_2 = Courier(
        id=5,
        courier_type="car",
        regions=[4, 11, 45],
        working_hours=["08:00-14:00"],
    )
    order_db_1 = Order(
        id=1,
        weight=40,
        region=4,
        delivery_hours=["09:30-12:30"],
        assign_time=datetime.strptime("2021-01-10T09:32:14.42Z", "%Y-%m-%dT%H:%M:%S.%fZ"),
        courier_id=5
    )
    migrated_db_session.add(courier_db_1)
    migrated_db_session.add(courier_db_2)
    migrated_db_session.add(order_db_1)
    migrated_db_session.commit()

    response = await api_client.post("/orders/complete",
                                        json={
                                            "courier_id": 6,
                                            "order_id": 1,
                                            "complete_time": "2021-01-10T10:33:01.42Z"
                                        })
    assert response.status_code == 400