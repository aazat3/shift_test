import pytest

from shift_test.src.crud.user import (
    create_user,
    get_user_by_username,
)
from shift_test.src.core.security import password_hash 


@pytest.mark.asyncio
async def test_create_user(session):
    user = await create_user(
        session=session,
        username="test",
        password_hash=password_hash(
            "123456"
        ),
    )

    assert user.id is not None
    assert user.username == "test"


@pytest.mark.asyncio
async def test_get_user_by_username(
    session,
):
    await create_user(
        session=session,
        username="test",
        password_hash="hash",
    )

    user = await get_user_by_username(
        session,
        "test",
    )

    assert user is not None
    assert user.username == "test"