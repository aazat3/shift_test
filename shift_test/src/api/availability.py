from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from shift_test.src.db.session import get_session
from shift_test.src.crud.availability import check_room_slot_availability_by_date, get_room_availability_by_room_id_by_date, get_all_availability_by_date
from shift_test.src.core.security import get_current_user
from shift_test.src.schemas.availability import RoomAvailability, RoomSlotAvailabilityResponse


router = APIRouter(prefix="/availability", tags=["Availability"])

# Возвращает список всех комнат с их слотами и информацией о том, доступны ли они для бронирования на указанную дату
@router.get("/", response_model=list[RoomAvailability])
async def get_available_rooms(
    date: date,
    session: AsyncSession = Depends(get_session),
):
    result = await get_all_availability_by_date(
        session,
        date
    )

    if not result:
        raise HTTPException(
            404,
            "No rooms found"
        )

    return result


@router.get("/rooms/{room_id}", response_model=RoomAvailability)
async def get_room_available_room_slots(
    room_id:int,
    booking_date:date,
    session:AsyncSession=Depends(get_session),
):
    result = await get_room_availability_by_room_id_by_date(
        session,
        room_id,
        booking_date
    )

    if not result:
        raise HTTPException(
            404,
            "Room not found"
        )
    
    return result


@router.get("/room_slots/{room_slot_id}", response_model=RoomSlotAvailabilityResponse)
async def get_room_slot_availability(
    room_slot_id:int,
    booking_date:date,
    session:AsyncSession=Depends(get_session),
):
    available = await check_room_slot_availability_by_date(
        session,
        room_slot_id,
        booking_date
    )

    return {
        "room_slot_id": room_slot_id,
        "booking_date": booking_date,
        "available": available,
    }