import pytest
from test.test_data import generate_courier


@pytest.mark.asyncio
async def test_import_couriers_single(api_client):
    courier = generate_courier()

    response = await api_client.post(
        "/couriers",
        json = {
            "data": [
                {
                    "courier_id": courier['courier_id'],
                    "courier_type": courier['courier_type'],
                    "regions": courier['regions'],
                    "working_hours": courier['working_hours']
                }
            ]
        }
    )
    
    assert response.status_code == 201
    assert response.json() == {"couriers": [{"id": courier["courier_id"]}]}

@pytest.mark.asyncio
async def test_import_couriers_many(api_client):
    couriers = [generate_courier() for _ in range(10)]

    request = {"data": []}
    result = {"couriers": []}

    for courier in couriers:
        request["data"].append({
                                "courier_id": courier['courier_id'],
                                "courier_type": courier['courier_type'],
                                "regions": courier['regions'],
                                "working_hours": courier['working_hours']
                                })
        result["couriers"].append({
                                   "id": courier['courier_id']
                                    })

    response = await api_client.post(
        "/couriers",
        json = request
    )
    
    assert response.status_code == 201
    assert response.json() == result

@pytest.mark.asyncio
async def test_import_couriers_bad_req(api_client):
    courier = generate_courier()

    response = await api_client.post(
        "/couriers",
        json = {
            "data": [
                {
                    "courier_id": courier['courier_id'],
                    "courier_type": courier['courier_type'],
                    "regions": courier['regions'],
                    "working_hours": courier['working_hours'],
                    "add_val": "test"
                }
            ]
        }
    )
    
    assert response.status_code == 400
    assert response.json() == {"validation_error": {"couriers": [{"id": courier["courier_id"], "add_val": "test"}]}}