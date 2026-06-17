import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_rooms(
    auth_client: AsyncClient,
):

    response = await auth_client.get(
        "/api/rooms",
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list
    )