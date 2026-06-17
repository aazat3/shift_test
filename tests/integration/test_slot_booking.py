from datetime import date, time

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from shift_test.src.models.room import Room
from shift_test.src.models.room_slot import RoomSlot

@pytest.mark.asyncio
async def test_slot_unavailable_after_booking(
    auth_client: AsyncClient,
    session: AsyncSession
):
    today = str(date.today())

    room = Room(
        title="Room A"
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

    await auth_client.post(
        "/api/bookings",

        json={
            "room_slot_id":1,
            "booking_date":today
        }
    )

    response = await auth_client.get(
        "/api/availability/room_slots/1",

        params={
            "booking_date": today
        }
    )

    assert response.status_code == 200

    data=response.json()

    assert data["available"] is False



@pytest.mark.asyncio
async def test_admin_create_slot(
    admin_client: AsyncClient,
    session: AsyncSession
):
    room = Room(
        title="Room A"
    )

    session.add(room)

    await session.commit()
    await session.refresh(room)

    response = await admin_client.post(
        f"/api/room_slots",
        json={
            "room_id":room.id,
            "start_time":"09:00",
            "end_time":"11:00"
        }
    )

    assert response.status_code == 201

    response = await admin_client.get(
        f"/api/room_slots/{room.id}/room_slots"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list
    )


@pytest.mark.asyncio
async def test_user_cannot_create_slot(
    auth_client: AsyncClient,
    session: AsyncSession
):
    room = Room(
        title="Room A"
    )

    session.add(room)

    await session.commit()
    await session.refresh(room)
    response = await auth_client.post(
        f"/api/room_slots",
        json={
            "room_id":room.id,
            "start_time":"09:00",
            "end_time":"11:00"
        }
    )

    assert response.status_code == 403