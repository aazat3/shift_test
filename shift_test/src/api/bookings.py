from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from shift_test.src.crud.booking import create_booking, get_bookings, get_booking_by_id, get_bookings_by_user, delete_booking
from shift_test.src.models.user import User
from shift_test.src.schemas.booking import BookingCreate, BookingCreateWithoutUser, BookingRead, BookingUpdate
from shift_test.src.db.session import get_session
from shift_test.src.core.security import get_current_user

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.post(
    "/",
    response_model=BookingRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_booking_endpoint(
    data: BookingCreateWithoutUser,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    
    booking = await create_booking(
        session=session,
        data=data,
        user=user,
    )
    return booking


@router.get("/", response_model=list[BookingRead])
async def list_bookings_endpoint(
    session: AsyncSession = Depends(get_session),
):
    return await get_bookings(session)


@router.get(
    "/my",
    response_model=list[BookingRead]
)
async def my_bookings_endpoint(
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
):
    result = await get_bookings_by_user(
        session,
        user=user,
    )

    return result


@router.get("/{booking_id}", response_model=BookingRead)
async def get_booking_endpoint(
    booking_id: int, session: AsyncSession = Depends(get_session),
):
    booking = await get_booking_by_id(session, booking_id)
    if booking is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
    return booking


# @router.put("/{booking_id}", response_model=BookingRead)
# async def update_booking_endpoint(
#     booking_id: int,
#     data: BookingUpdate,
#     session: AsyncSession = Depends(get_session),
# ):
#     booking = await get_booking_by_id(session, booking_id)
#     if not booking:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
#     return await update_booking(session, booking, data)


@router.delete(
    "/{booking_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def cancel_booking_endpoint(
    booking_id: int,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    
    booking = await get_booking_by_id(
        session,
        booking_id,
    )

    if booking is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
    
    await delete_booking(
        session,
        booking,
        user=user,
    )
