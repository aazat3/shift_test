from datetime import datetime, date

from sqlalchemy import DateTime, Integer, UniqueConstraint, func, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from shift_test.src.db.base import Base
from shift_test.src.models import user, room_slot, room


class Booking(Base):
    __tablename__ = "bookings"
    __table_args__ = (
        UniqueConstraint(
            "room_slot_id",
            "booking_date",
            name="uq_room_slot_booking_date"
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)    
    room_slot_id: Mapped[int] = mapped_column(ForeignKey("room_slots.id", ondelete="CASCADE"), nullable=False)
    booking_date: Mapped[date] = mapped_column(Date)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    user: Mapped["user.User"] = relationship(
        back_populates="bookings"
    )

    room_slot: Mapped["room_slot.RoomSlot"] = relationship(
        back_populates="bookings",
        lazy="selectin" # Т.к. в большинстве случаев при работе с бронированиями нам будет нужна информация о слоте, то стоит подгружать его сразу, чтобы не делать лишних запросов к БД
    )

    room: Mapped["room.Room"] = relationship(
        back_populates="bookings"
    )