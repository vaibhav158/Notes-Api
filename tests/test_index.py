from httpx import AsyncClient
import pytest


@pytest.mark.anyio
async def test_index_route_success(client: AsyncClient):

    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello, World!"
    }