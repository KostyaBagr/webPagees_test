
from sqlalchemy import Column, Integer, String, DateTime, func, BigInteger
from sqlalchemy.orm import DeclarativeBase



class Base(DeclarativeBase):
    pass


class User(Base):
    """Таблица хранит данные о пользователе"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, index=True, unique=True)
    name = Column(String, nullable=True)
    username = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
