from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from shift_test.src.core.security import get_admin_rights, get_current_user
from shift_test.src.crud.room import *
from shift_test.src.db.session import get_session
from shift_test.src.schemas.room import RoomCreate, RoomRead, RoomReadWithRelationships, RoomUpdate


router = APIRouter(prefix="/rooms", tags=["rooms"])


@router.post("", response_model=RoomRead, status_code=status.HTTP_201_CREATED)
async def create_room_endpoint(
    payload: RoomCreate, session: AsyncSession = Depends(get_session),
    admin=Depends(get_admin_rights),
):
    if payload.title is not None:
        existing = await get_room_by_title(session, payload.title)
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Room with title already exists")
    return await create_room(session, payload)


@router.get("", response_model=list[RoomRead])
async def list_rooms_endpoint(
    session: AsyncSession = Depends(get_session), 
):
    return await get_rooms(session)


@router.get("/", response_model=list[RoomReadWithRelationships])
async def list_rooms_with_room_slots_endpoint(
    session: AsyncSession = Depends(get_session), 
):
    return await get_rooms_with_room_slots(session)


@router.get("/{room_id}", response_model=RoomRead)
async def get_room_endpoint(
    room_id: int, session: AsyncSession = Depends(get_session), 
):
    room = await get_room_by_id(session, room_id)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return room


@router.put("/{room_id}", response_model=RoomRead)
async def update_room_endpoint(
    room_id: int,
    payload: RoomUpdate,
    session: AsyncSession = Depends(get_session),
    admin=Depends(get_admin_rights),
):
    room = await get_room_by_id(session, room_id)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    if payload.title is not None and payload.title != room.title:
        existing = await get_room_by_title(session, payload.title)
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Room with title already exists")
    return await update_room(session, room, payload)


@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_room_endpoint(
    room_id: int, session: AsyncSession = Depends(get_session), 
    admin=Depends(get_admin_rights)
):
    room = await get_room_by_id(session, room_id)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    await delete_room(session, room)
