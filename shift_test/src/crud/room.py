from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from shift_test.src.models.room import Room
from shift_test.src.schemas.room import RoomCreate, RoomUpdate


async def create_room(session: AsyncSession, data: RoomCreate) -> Room:
    room = Room(**data.model_dump())
    session.add(room)
    await session.commit()
    await session.refresh(room)
    return room


async def get_rooms(session: AsyncSession) -> list[Room]:
    result = await session.execute(select(Room))
    return list(result.scalars().all())


async def get_room_by_id(session: AsyncSession, room_id: int) -> Optional[Room]:
    result = await session.get(Room, room_id)
    return result


async def get_room_by_title(session: AsyncSession, title: str) -> Optional[Room]:
    result = await session.execute(select(Room).where(Room.title == title))
    return result.scalars().first()


async def get_rooms_with_room_slots(session: AsyncSession) -> list[Room]:
    result = await session.execute(select(Room).options(selectinload(Room.room_slots)))
    return list(result.scalars().all())


async def update_room(
    session: AsyncSession, room: Room, data: RoomUpdate
) -> Room:
    for field, value in data.model_dump().items():
        setattr(room, field, value)
    await session.commit()
    await session.refresh(room)
    return room


async def delete_room(session: AsyncSession, room: Room) -> None:
    await session.delete(room)
    await session.commit()

