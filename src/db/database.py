from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.core.config import db_settings

engine = create_async_engine(db_settings.DB_URL)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession)
