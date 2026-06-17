import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_register(
    async_client: AsyncClient
):
    response = await async_client.post(
        "/api/auth/register",
        json={
            "username": "user",
            "password": "123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == "user"



@pytest.mark.asyncio
async def test_login(
    async_client: AsyncClient
):
    await async_client.post(
        "/api/auth/register",
        json={
            "username": "user",
            "password": "123"
        }
    )

    response = await async_client.post(
        "/api/auth/login",
        json={
            "username": "user",
            "password": "123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "users_access_token" in data
