from sqlalchemy.ext.asyncio import AsyncSession

from database import Storage, SQLAlchemyStorage, engine

storage: Storage = SQLAlchemyStorage(lambda: AsyncSession(engine))
