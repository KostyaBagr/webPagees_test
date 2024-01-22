from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from database_conf import engine
from task2.models import User


def create_user(data: dict):
    """Function to create a user"""
    Session = sessionmaker(bind=engine)
    with Session() as session:
        db_user = User(name=data['name'], username=data['username'], telegram_id=data['telegram_id'])
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user


def user_exists(telegram_id: int):
    """Функция проверят существует ли юзер"""
    Session = sessionmaker(bind=engine)
    with Session() as session:
        user = session.execute(select(User).where(User.telegram_id == telegram_id))
        return user.scalars().first()