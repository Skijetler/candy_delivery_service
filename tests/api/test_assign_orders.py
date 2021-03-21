import pytest

from candy_delivery.db.models import Courier, Order


@pytest.mark.asyncio
async def test_assign_orders_courier_not_found(api_client):
    response = await api_client.post("/orders/assign",
                                        json={
                                            "courier_id": 0
                                        })
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_assign_orders(api_client, migrated_db_session):
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
        delivery_hours=["09:30-12:30"]
    )
    order_db_2 = Order(
        id=2,
        weight=14,
        region=20,
        delivery_hours=["14:30-16:00"]
    )
    order_db_3 = Order(
        id=3,
        weight=16,
        region=15,
        delivery_hours=["12:00-15:30"]
    )
    order_db_4 = Order(
        id=4,
        weight=10,
        region=9,
        delivery_hours=["08:00-08:30"]
    )

    migrated_db_session.add(courier_db)
    migrated_db_session.add(order_db_1)
    migrated_db_session.add(order_db_2)
    migrated_db_session.add(order_db_3)
    migrated_db_session.add(order_db_4)
    migrated_db_session.commit()

    response = await api_client.post("/orders/assign",
                                        json={
                                            "courier_id": courier_db.id
                                        })
    assert response.status_code == 200

    assigned_orders_ids = [order.id for order in migrated_db_session.query(Order).filter(Order.courier_id == courier_db.id)]
    assert assigned_orders_ids == [1,2,3]

@pytest.mark.asyncio
async def test_assign_orders_not_found(api_client, migrated_db_session):
    courier_db = Courier(
        id=6,
        courier_type="car",
        regions=[20, 15, 9, 4],
        working_hours=["09:00-16:00"],
    )
    order_db_1 = Order(
        id=1,
        weight=10,
        region=9,
        delivery_hours=["08:00-08:30"]
    )

    migrated_db_session.add(courier_db)
    migrated_db_session.add(order_db_1)
    migrated_db_session.commit()

    response = await api_client.post("/orders/assign",
                                        json={
                                            "courier_id": courier_db.id
                                        })
    assert response.status_code == 200

    assigned_orders_ids = [order.id for order in migrated_db_session.query(Order).filter(Order.courier_id == courier_db.id)]
    assert assigned_orders_ids == []