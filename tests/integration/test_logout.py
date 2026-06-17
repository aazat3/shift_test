import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_logout(
    auth_client: AsyncClient
):


    response = await auth_client.post(
        "/api/auth/logout"
    )


    assert response.status_code == 200


    assert (
        "users_access_token"
        not in auth_client.cookies
    )