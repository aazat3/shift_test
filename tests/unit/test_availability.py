from datetime import date, time

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from shift_test.src.crud.availability import check_room_slot_availability_by_date
from shift_test.src.models.user import User
from shift_test.src.models.room import Room
from shift_test.src.models.room_slot import RoomSlot

from shift_test.src.crud.booking import (
    create_booking,
)
from shift_test.src.schemas.booking import BookingCreateWithoutUser

@pytest.mark.asyncio
async def test_slot_available(
    session: AsyncSession,
):

    room = Room(
        title="Test room"
    )

    session.add(room)

    await session.commit()

    slot = RoomSlot(
        room_id=room.id,
        start_time=time(9, 0),
        end_time=time(11, 0),
    )

    session.add(slot)

    await session.commit()

    available = await check_room_slot_availability_by_date(
        session,
        slot.id,
        date.today(),
    )

    assert available is True


@pytest.mark.asyncio
async def test_slot_not_available(
    session,
):

    user = User(
        username="user",
        password_hash="123"
    )

    room = Room(
        title="Room"
    )

    session.add_all(
        [
            user,
            room,
        ]
    )

    await session.commit()

    slot = RoomSlot(
        room_id=room.id,
        start_time=time(9, 0),
        end_time=time(11, 0),
    )

    session.add(slot)

    await session.commit()

    await create_booking(
        session=session,
        data=BookingCreateWithoutUser(
            room_slot_id=slot.id,
            booking_date=date.today(),
        ),
        user=user,
    )

    available = await check_room_slot_availability_by_date(
        session,
        slot.id,
        date.today(),
    )

    assert available is False