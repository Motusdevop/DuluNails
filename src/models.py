from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import Optional
from datetime import datetime

class Base(DeclarativeBase): pass

class Appointment(Base):
    __tablename__ = 'appointment'

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime]
    active: Mapped[bool] = False
    user_id = Mapped[Optional[int]]

class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    telegram_id: Mapped[int]
    phone: Mapped[str]
    active_appointment_id : Mapped[Optional[int]]
    banned: Mapped[bool] = False

