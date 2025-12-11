from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from config import settings_db


async_engine = create_async_engine(url=settings_db.async_db_URL, echo=True)
async_session = async_sessionmaker(async_engine)

# Основной класс для создания моделей таблиц БД
class Base(DeclarativeBase):
    metadata = MetaData()