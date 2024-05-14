import datetime

from sqlalchemy import select

from models import User, Window

from database import session_factory, create_tables

from exceptions import UserNotFound


class UserRepository:

    @classmethod
    def check_register(cls, telegram_id: int) -> bool:
        with session_factory() as session:
            query = select(User).where(User.telegram_id == telegram_id)

            result = session.execute(query)

            if result.one_or_none():
                return True
            else:
                return False

    @classmethod
    def check_admin(cls, telegram_id: int) -> bool:
        with session_factory() as session:
            query = select(User).where(User.telegram_id == telegram_id)

            result = session.execute(query)

            if result.one_or_none():
                if result[0].is_admin:
                    return True
            else:
                return False

    @classmethod
    def make_admin(cls, telegram_id: int):
        with session_factory() as session:
            query = select(User).where(User.telegram_id == telegram_id)

            result = session.execute(query)

            if result.one_or_none():
                user = result.one_or_none()[0]
                user.is_admin = True
                session.commit()

            else:
                raise UserNotFound


    @classmethod
    def register_user(cls, **kwargs):
        user = User(**kwargs)

        with session_factory() as session:
            session.add(user)
            session.commit()

    @classmethod
    def get_user(cls, telegram_id: int) -> User | None:

        with session_factory() as session:
            query = session.query(User).filter(User.telegram_id == telegram_id)
            res = session.execute(query).first()

            if res:
                user = res[0]
                return user

            else:
                return None

    @classmethod
    def get_all_telegram_id(cls) -> list[int]:

        with session_factory() as session:
            query = select(User.telegram_id)
            res = session.execute(query).all()
            telegram_id_list: list[int] = [id[0] for id in res]
            return telegram_id_list

    @classmethod
    def get_all_banned(cls) -> list[User]:

        with session_factory() as session:
            query = select(User).where(User.is_banned)

            res = session.execute(query).all()
            banned_list: list[User] = [user[0] for user in res]

            return banned_list

    @classmethod
    def ban(cls, username: str):

        with session_factory() as session:
            try:
                query = select(User).where(User.username == username)
                res = session.execute(query).first()
                user = res[0]
                user.is_banned = True
                user.ban_datetime = datetime.datetime.now()

                session.commit()
            except TypeError:
                raise UserNotFound
    @classmethod
    def unban(cls, username: str):

        with session_factory() as session:
            try:
                query = select(User).where(User.username == username)
                res = session.execute(query).first()
                user = res[0]
                user.is_banned = False
                user.ban_datetime = None

                session.commit()
            except TypeError:
                raise UserNotFound

class WindowRepository:

    @classmethod
    def create_window(cls, appointment: Window):
        with session_factory() as session:
            session.add(appointment)
            session.commit()

    @classmethod
    def get_all_windows(cls) -> list[Window]:

        query = select(Window)

        with session_factory() as session:
            res = session.execute(query)

            windows = list()

            for window in res.all():
                obj: Window = window[0]
                windows.append(obj)

            return windows
    @classmethod
    def get_all_no_active_windows(cls) -> list[Window]:

        query = select(Window).where(Window.active == False)

        with session_factory() as session:
            res = session.execute(query)

            windows = list()

            for window in res.all():
                obj: Window = window[0]
                windows.append(obj)

            return windows
    @classmethod
    def get_window(cls, id: int) -> Window | None:

        query = select(Window).where(Window.id == id)

        with session_factory() as session:
            res = session.execute(query)
            window = res.one_or_none()

            if window:
                return window[0]

            return window

    @classmethod
    def update_window(cls, id: int, data: dict):

        with session_factory() as session:
            query = session.query(Window).filter(Window.id == id)
            res = session.execute(query)
            window: Window = res.first()[0]
            window.active = data['active']
            window.user_id = data['user_id']
            window.correct_time = data['correct_time']
            session.commit()

    @classmethod
    def delete_window(cls, id: int):

        window = WindowRepository.get_window(id)

        with session_factory() as session:
            session.delete(window)
            session.commit()
    @classmethod
    def cancel_window(cls, id: int):

        with session_factory() as session:
            query = session.query(Window).filter(Window.id == id)
            res = session.execute(query)
            window: Window = res.first()[0]
            window.active = False
            window.user_id = None
            window.correct_time = None
            session.commit()

    @classmethod
    def all_window_per_user(cls, telegram_id: int) -> list[Window]:
        user = UserRepository.get_user(telegram_id=telegram_id)

        with session_factory() as session:
            query = select(Window).where(Window.user_id == telegram_id)
            res = session.execute(query).all()
            windows: list[Window] = [window[0] for window in res]
            return windows




if __name__ == '__main__':
    create_tables()
    # UserRepository.register_user(12334344)
    # # print(UserRepository.check_register(12334344))
    #
    # window = Window(datetime=datetime.datetime(year=2024, month=2, day=17))
    # WindowRepository.create_window(window)
    # # WindowRepository.create_window(date='02.10 с 17:00')
    # print(WindowRepository.get_all_windows())
    # print(WindowRepository.get_window(id=2))

    UserRepository.get_all_telegram_id()
