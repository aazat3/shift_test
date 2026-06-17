from datetime import time
from pydantic import BaseModel, ConfigDict


class RoomSlotBase(BaseModel):
    room_id: int
    start_time: time
    end_time: time

    model_config = ConfigDict(from_attributes=True)

class RoomSlotCreate(RoomSlotBase):
    pass

class RoomSlotRead(RoomSlotBase):
    id: int



class RoomSlotUpdate(BaseModel):
    id: int
    start_time: time 
    end_time: time 
