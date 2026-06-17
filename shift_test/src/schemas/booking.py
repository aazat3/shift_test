from datetime import datetime, time, date
from pydantic import BaseModel, ConfigDict

from shift_test.src.schemas.room_slot import RoomSlotRead


class BookingBase(BaseModel):
    room_id:int
    user_id:int
    room_slot_id:int
    booking_date: date

    model_config = ConfigDict(from_attributes=True)


class BookingCreateWithoutUser(BaseModel):
    room_slot_id:int
    booking_date: date

    model_config = ConfigDict(from_attributes=True)


class BookingCreate(BookingBase):
    pass


class BookingRead(BookingBase):
    id: int
    room_slot: RoomSlotRead
    created_at: datetime


class BookingUpdate(BookingBase):
    pass


