from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from shift_test.src.db.base import Base
from shift_test.src.models import booking

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String)

    # Простой флаг для определения, является ли пользователь администратором. 
    # В реальной жизни может быть более сложная система ролей и прав доступа, но для нашего тестового задания этого достаточно.
    is_administrator: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False) 

    bookings: Mapped[list["booking.Booking"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
