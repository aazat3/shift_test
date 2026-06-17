import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_register(
    async_client: AsyncClient
):
    response = await async_client.post(
        "/api/auth/register",
        json={
            "username": "test",
            "password": "123456"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == "test"



@pytest.mark.asyncio
async def test_login(
    async_client: AsyncClient
):
    await async_client.post(
        "/api/auth/register",
        json={
            "username": "test",
            "password": "123456"
        }
    )

    response = await async_client.post(
        "/api/auth/login",
        json={
            "username": "test",
            "password": "123456"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "users_access_token" in data
