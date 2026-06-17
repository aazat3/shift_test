from datetime import date
from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from shift_test.src.models.booking import Booking
from shift_test.src.models.user import User
from shift_test.src.schemas.booking import BookingCreate, BookingCreateWithoutUser
from shift_test.src.crud.room_slot import get_room_slot_by_id


async def create_booking(
    session: AsyncSession, 
    data: BookingCreateWithoutUser, 
    user: User,
) -> Booking:
    
    room_slot = await get_room_slot_by_id(
        session,
        data.room_slot_id,
    )
 
    if room_slot is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room slot not found",
        )

    occupied = await booking_exists(
        session,
        room_slot_id=data.room_slot_id,
        booking_date=data.booking_date,
    )

    if occupied:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Room slot already booked",
        )

    new_data: BookingCreate = BookingCreate(
        user_id=user.id,
        room_id=room_slot.room_id,
        **data.model_dump(),
    )
    
    booking = Booking(**new_data.model_dump())
    session.add(booking)
    await session.commit()
    await session.refresh(booking)
    return booking


async def get_bookings(session: AsyncSession) -> list[Booking]:
    # result = await session.execute(select(Booking))
    result = await session.execute(select(Booking).options(selectinload(Booking.room_slot), selectinload(Booking.room)))
    return list(result.scalars().all())


async def get_booking_by_id(session: AsyncSession, booking_id: int) -> Optional[Booking]:
    result = await session.get(Booking,  booking_id)
    return result


async def get_bookings_by_user(
    session: AsyncSession, user: User
) -> List[Booking]:
    result = await session.execute(
        select(Booking).where(Booking.user_id == user.id)
    )
    return list(result.scalars().all())


async def get_bookings_by_room_id(
    session: AsyncSession, room_id: int
) -> List[Booking]:
    result = await session.execute(
        select(Booking).where(Booking.room_id == room_id)
    )
    return list(result.scalars().all())

async def get_bookings_by_booking_date(
    session: AsyncSession, booking_date: date
) -> List[Booking]:
    result = await session.execute(
        select(Booking).where(Booking.booking_date == booking_date)
    )
    return list(result.scalars().all())


async def booking_exists(
    session: AsyncSession,
    *,
    room_slot_id: int,
    booking_date: date,
) -> bool:
    stmt = select(Booking).where(
        Booking.room_slot_id == room_slot_id,
        Booking.booking_date == booking_date,
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none() is not None


# async def update_booking(
#     session: AsyncSession, booking: Booking, data: BookingUpdate
# ) -> Booking:
#     for field, value in data.model_dump().items():
#         setattr(booking, field, value)
#     await session.commit()
#     await session.refresh(booking)
#     return booking


async def delete_booking(
    session: AsyncSession, 
    booking: Booking, 
    user: User,
) -> None:
    
    if (
        booking.user_id != user.id
        and not user.is_administrator
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden",
        )

    await session.delete(booking)
    await session.commit()

