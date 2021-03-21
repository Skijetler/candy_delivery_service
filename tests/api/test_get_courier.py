import pytest
from random import randint

from test.test_data import generate_courier_db
from candy_delivery.db.models import Courier


@pytest.mark.asyncio
async def test_get_courier(api_client, migrated_db_session):
    courier = generate_courier_db()

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

    response = await api_client.get("/couriers/" + str(courier["courier_id"]))
    assert response.status_code == 200
    assert response.json() == {
        "courier_id": courier["courier_id"],
        "courier_type": courier["courier_type"],
        "regions": courier["regions"],
        "working_hours": courier["working_hours"],
        "rating": courier["rating"],
        "earnings": courier["earnings"]
    }

@pytest.mark.asyncio
async def test_get_courier_not_found(api_client):
    response = await api_client.get("/couriers/" + str(randint(0, 100)))
    assert response.status_code == 404