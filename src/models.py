from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import Optional
from datetime import datetime as dt
from datetime import time


from exceptions import UncorrectFormat

class Base(DeclarativeBase): pass

class Window(Base):
    __tablename__ = 'window'

    id: Mapped[int] = mapped_column(primary_key=True)
    datetime: Mapped[dt]
    active: Mapped[bool] = mapped_column(default=False)
    completed: Mapped[bool] = mapped_column(default=False)
    user_id: Mapped[Optional[int]]
    correct_time: Mapped[Optional[time]]
    @classmethod
    def str_to_datetime(cls, string: str) -> dt:
        try:
            string = f'{dt.now().year} ' + string
            date = dt.strptime(string,'%Y %d.%m %H:%M')

            return date
        except:
            raise UncorrectFormat
    @classmethod
    def datetime_to_str(cls, date: dt) -> str:
        string = date.strftime("%d.%m c %H:%M до 20:00")

        return string

class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    fullname: Mapped[str]
    username: Mapped[str]
    telegram_id: Mapped[int]
    phone: Mapped[str]
    is_banned: Mapped[bool] = mapped_column(default=False)
    ban_datetime: Mapped[Optional[dt]]

