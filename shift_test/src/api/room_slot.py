from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from shift_test.src.core.security import get_admin_rights, get_current_user
from shift_test.src.crud.room_slot import get_room_slots_by_room_id, create_room_slot, get_room_slots, get_room_slot_by_id, delete_room_slot, update_room_slot
from shift_test.src.schemas.room_slot import RoomSlotCreate, RoomSlotRead, RoomSlotUpdate
from shift_test.src.db.session import get_session

router = APIRouter(prefix="/room_slots", tags=["room_slots"])


@router.post(
    "/",
    response_model=RoomSlotRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_room_slot_endpoint(
    data: RoomSlotCreate,
    session: AsyncSession = Depends(get_session),
    admin=Depends(get_admin_rights),

):
    
    room_slot = await create_room_slot(
        session=session,
        data=data,
    )
    return room_slot


@router.get("/", response_model=list[RoomSlotRead])
async def list_room_slots_endpoint(
    session: AsyncSession = Depends(get_session),
):
    return await get_room_slots(session)


@router.get("/{room_id}/room_slots", response_model=list[RoomSlotRead])
async def get_room_slot_endpoint(
    room_id: int, session: AsyncSession = Depends(get_session),
):
    room_slots = await get_room_slots_by_room_id(session, room_id=room_id)
    if room_slots is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="RoomSlots not found")
    return room_slots


@router.put("/{room_slot_id}", response_model=RoomSlotRead)
async def update_room_slot_endpoint(
    room_slot_id: int,
    data: RoomSlotUpdate,
    session: AsyncSession = Depends(get_session),
    admin=Depends(get_admin_rights),
):
    room_slot = await get_room_slot_by_id(session, room_slot_id)
    if not room_slot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return await update_room_slot(session, room_slot, data)


@router.delete(
    "/{room_slot_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def cancel_room_slot_endpoint(
    room_slot_id: int,
    session: AsyncSession = Depends(get_session),
    admin=Depends(get_admin_rights),
):
    
    room_slot = await get_room_slot_by_id(
        session,
        room_slot_id,
    )

    if room_slot is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="RoomSlot not found")
    
    await delete_room_slot(
        session,
        room_slot,
    )
