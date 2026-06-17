from datetime import date
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession


from shift_test.src.models.booking import Booking
from shift_test.src.models.room import Room
from shift_test.src.models.room_slot import RoomSlot


async def get_booked_room_slots_by_room_id_by_date(
    session: AsyncSession,
    room_id: int,
    booking_date: date,
):
    stmt = (
        select(Booking.room_slot_id)
        .join(
            RoomSlot,
            Booking.room_slot_id == RoomSlot.id
        )
        .where(
            RoomSlot.room_id == room_id,
            Booking.booking_date == booking_date
        )
    )

    result = await session.execute(stmt)
    return list(result.scalars().all())



async def get_room_availability_by_room_id_by_date(
    session: AsyncSession,
    room_id: int,
    booking_date: date,
):
    stmt = (
        select(Room)
        .where(
            Room.id == room_id
        )
        .options(
            selectinload(Room.room_slots)
        )
    )

    result = await session.execute(stmt)
    room = result.scalar_one_or_none()

    if not room:
        return None

    booked_room_slots = await get_booked_room_slots_by_room_id_by_date(
        session,
        room_id,
        booking_date
    )

    return {
        "room_id": room.id,
        "room_title": room.title,

        "room_slots":[
            {
                "room_slot_id":slot.id,
                "start_time":slot.start_time,
                "end_time":slot.end_time,
            }

            for slot in room.room_slots if slot.id not in booked_room_slots
        ]
    }


async def get_all_availability_by_date(
    session: AsyncSession,
    booking_date: date,
):
    stmt = (
        select(Room)
        .options(
            selectinload(Room.room_slots)
        )
    )

    result = await session.execute(stmt)
    rooms = result.scalars().all()
    response=[]

    for room in rooms:
        booked_room_slots = await get_booked_room_slots_by_room_id_by_date(
            session,
            room.id,
            booking_date
        )

        response.append(
            {
                "room_id":room.id,
                "room_title":room.title,

                "room_slots":[
                    {
                        "room_slot_id":slot.id,
                        "start_time":slot.start_time,
                        "end_time":slot.end_time,
                    }
                    for slot in room.room_slots if slot.id not in booked_room_slots
                ]
            }
        )

    return response


# async def check_room_slot_availability_by_date(
#     session: AsyncSession,
#     room_slot_id:int,
#     booking_date:date,
# ):

#     stmt = (
#         select(Booking)
#         .where(
#             Booking.room_slot_id == room_slot_id,
#             Booking.booking_date == booking_date
#         )
#     )

#     result = await session.execute(stmt)

#     return result.scalar_one_or_none()