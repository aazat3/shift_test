# from datetime import date

# import pytest

# from shift_test.src.models.user import User
# from shift_test.src.models.room import Room
# from shift_test.src.models.room_slot import RoomSlot

# from shift_test.src.crud.booking import (
#     create_booking,
# )

# @pytest.mark.asyncio
# async def test_slot_available(
#     session,
# ):

#     room = Room(
#         title="Test room"
#     )

#     session.add(room)

#     await session.commit()

#     slot = RoomSlot(
#         room_id=room.id,
#         start_time="09:00",
#         end_time="11:00",
#     )

#     session.add(slot)

#     await session.commit()

#     available = await check_room_slot_available_by_date(
#         session,
#         slot.id,
#         date.today(),
#     )

#     assert available is True