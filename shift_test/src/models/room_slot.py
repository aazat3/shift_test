from datetime import time

from sqlalchemy import Integer, Time, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from shift_test.src.db.base import Base
from shift_test.src.models import room, booking

class RoomSlot(Base):
    __tablename__ = "room_slots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False)
    start_time: Mapped[time] = mapped_column(Time)
    end_time: Mapped[time] = mapped_column(Time)

    room: Mapped["room.Room"]  = relationship(
        back_populates="room_slots"
    )

    bookings: Mapped[list["booking.Booking"]] = relationship(
        back_populates="room_slot"
    )