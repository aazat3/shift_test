from pydantic import BaseModel, ConfigDict

from shift_test.src.schemas import room_slot, booking


class RoomBase(BaseModel):
    title: str
    description: str | None

    model_config = ConfigDict(from_attributes=True)


class RoomCreate(RoomBase):
    pass

class RoomRead(RoomBase):
    id: int

class RoomReadWithRelationships(RoomRead):
    bookings: list["booking.BookingRead"]
    room_slots: list["room_slot.RoomSlotRead"]


class RoomUpdate(RoomBase):
    pass


