
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from shift_test.src.db.base import Base
from shift_test.src.models import booking, room_slot

class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(String ,nullable=True)

    room_slots: Mapped[list["room_slot.RoomSlot"]] = relationship(
        back_populates="room",
        cascade="all, delete-orphan"
    )

    bookings: Mapped[list["booking.Booking"]] = relationship(
        back_populates="room",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
