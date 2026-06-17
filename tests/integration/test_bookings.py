from datetime import date, time

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from shift_test.src.models.room import Room
from shift_test.src.models.room_slot import RoomSlot

@pytest.mark.asyncio
async def test_create_booking(
    auth_client: AsyncClient,
    session: AsyncSession
):
    room = Room(
        title="Test room"
    )

    session.add(room)

    await session.commit()
    await session.refresh(room)

    room_slot = RoomSlot(
        room_id=room.id,
        start_time=time(9, 0),
        end_time=time(11, 0),
    )

    session.add(room_slot)

    await session.commit()
    await session.refresh(room_slot)

    response = await auth_client.post(
        "/api/bookings",

        json={
            "room_slot_id":1,
            "booking_date":
                str(date.today())
        }
    )

    assert response.status_code == 201
    data=response.json()
    assert data["room_slot_id"] == 1


@pytest.mark.asyncio
async def test_duplicate_booking(
    auth_client: AsyncClient,
    session: AsyncSession
):

    room = Room(
        title="Test room"
    )

    session.add(room)

    await session.commit()
    await session.refresh(room)

    room_slot = RoomSlot(
        room_id=room.id,
        start_time=time(9, 0),
        end_time=time(11, 0),
    )

    session.add(room_slot)
    await session.commit()
    await session.refresh(room_slot)

    data={
        "room_slot_id":room_slot.id,
        "booking_date":
            str(date.today())
    }

    r1 = await auth_client.post(
        "/api/bookings",
        json=data
    )

    r2 = await auth_client.post(
        "/api/bookings",
        json=data
    )

    assert r1.status_code == 201
    assert r2.status_code == 409

