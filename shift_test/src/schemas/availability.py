from datetime import time, date
from pydantic import BaseModel, ConfigDict


class RoomSlotAvailability(BaseModel):
    room_slot_id: int
    start_time: time
    end_time: time

    model_config = ConfigDict(from_attributes=True)


class RoomAvailability(BaseModel):
    room_id: int
    room_title: str
    room_slots: list[RoomSlotAvailability]

    model_config = ConfigDict(from_attributes=True)


class RoomSlotAvailabilityResponse(BaseModel):
    room_slot_id: int
    booking_date: date
    available: bool

    model_config = ConfigDict(from_attributes=True)