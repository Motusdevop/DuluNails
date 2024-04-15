from sqlalchemy import select

from models import User

from database import session_factory, create_tables

class UserRepository:

    @classmethod
    def check_register(cls, telegram_id: int):
        with session_factory() as session:
            query = select(User).where(User.telegram_id == telegram_id)

            result = session.execute(query)

            if result.one_or_none():
                return True
            else:
                return False

    @classmethod
    def register_user(cls, username: str, telegram_id: int, phone: str):
        user = User(username=username, telegram_id=telegram_id, phone=phone, banned=False)

        with session_factory() as session:
            session.add(user)
            session.commit()

if __name__ == '__main__':
    create_tables()
    UserRepository.register_user(12334344)
    print(UserRepository.check_register(12334344))
