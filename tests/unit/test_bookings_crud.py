from datetime import date, time
import pytest
from sqlalchemy.ext.asyncio import AsyncSession


from shift_test.src.models.user import User
from shift_test.src.models.room import Room
from shift_test.src.models.room_slot import RoomSlot

from shift_test.src.crud.booking import (
    create_booking,
)
from shift_test.src.schemas.booking import BookingCreateWithoutUser


@pytest.mark.asyncio
async def test_create_booking(
    session: AsyncSession,
):

    user = User(
        username="user",
        password_hash="123",
    )

    room = Room(
        title="Room A",
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

    booking = await create_booking(
        session=session,
        data=BookingCreateWithoutUser(
            room_slot_id=slot.id,
            booking_date=date.today(),
        ),
        user=user,
    )

    assert booking.id is not None

    assert booking.user_id == user.id