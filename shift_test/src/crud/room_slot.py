from datetime import time
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from shift_test.src.models.room_slot import RoomSlot
from shift_test.src.schemas.room_slot import RoomSlotCreate, RoomSlotUpdate


async def create_room_slot(session: AsyncSession, data: RoomSlotCreate) -> RoomSlot:
    # По хорошему проверять пересечения по времени с существующими слотами, но для простоты пока не делаем этого
    room_slot = RoomSlot(**data.model_dump())
    session.add(room_slot)
    await session.commit()
    await session.refresh(room_slot)
    return room_slot


async def get_room_slots(session: AsyncSession) -> list[RoomSlot]:
    result = await session.execute(select(RoomSlot))
    return list(result.scalars().all())


async def get_room_slots_by_room_id(session: AsyncSession, room_id: int) -> list[RoomSlot]:
    result = await session.execute(select(RoomSlot).where(RoomSlot.room_id == room_id).order_by(RoomSlot.start_time))
    return list(result.scalars().all())


async def get_room_slot_by_id(session: AsyncSession, room_slot_id: int) -> Optional[RoomSlot]:
    result = await session.get(RoomSlot, room_slot_id)
    return result


async def room_slot_exists(
    session: AsyncSession,
    room_id: int,
    start_time: time,
    end_time: time,
):
    stmt = (
        select(RoomSlot)
        .where(
            RoomSlot.room_id == room_id,
            RoomSlot.start_time == start_time,
            RoomSlot.end_time == end_time,
        )
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none() is not None


async def update_room_slot(
    session: AsyncSession, room_slot: RoomSlot, data: RoomSlotUpdate
) -> RoomSlot:
    # По хорошему проверять пересечения по времени с существующими слотами, но для простоты пока не делаем этого
    for field, value in data.model_dump().items():
        setattr(room_slot, field, value)
    await session.commit()
    await session.refresh(room_slot)
    return room_slot


async def delete_room_slot(session: AsyncSession, room_slot: RoomSlot) -> None:
    await session.delete(room_slot)
    await session.commit()

