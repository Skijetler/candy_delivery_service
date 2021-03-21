import pytest
from test.test_data import generate_order


@pytest.mark.asyncio
async def test_import_orders_single(api_client):
    order = generate_order()

    response = await api_client.post(
        "/orders",
        json = {
            "data": [
                {
                    "order_id": order['order_id'],
                    "weight": order['weight'],
                    "region": order['region'],
                    "delivery_hours": order['delivery_hours']
                }
            ]
        }
    )
    
    assert response.status_code == 201
    assert response.json() == {"orders": [{"id": order["order_id"]}]}

@pytest.mark.asyncio
async def test_import_orders_many(api_client):
    orders = [generate_order() for _ in range(10)]

    request = {"data": []}
    result = {"orders": []}

    for order in orders:
        request["data"].append({
                                "order_id": order['order_id'],
                                "weight": order['weight'],
                                "region": order['region'],
                                "delivery_hours": order['delivery_hours']
                                })
        result["orders"].append({
                                 "id": order["order_id"]
                                })

    response = await api_client.post(
        "/orders",
        json = request
    )
    
    assert response.status_code == 201
    assert response.json() == result

@pytest.mark.asyncio
async def test_import_orders_bad_req(api_client):
    order = generate_order()

    response = await api_client.post(
        "/orders",
        json = {
            "data": [
                {
                    "order_id": order['order_id'],
                    "weight": order['weight'],
                    "region": order['region'],
                    "delivery_hours": order['delivery_hours'],
                    "rand_val": "test_100"
                }
            ]
        }
    )
    
    assert response.status_code == 400
    assert response.json() == {"validation_error": {"orders": [{"id": order["order_id"], "rand_val": "test_100"}]}}