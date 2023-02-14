import logging
from abc import ABC, abstractmethod
from types import TracebackType
from typing import Self, Callable, Any, Sequence

from sqlalchemy import select, update, Row, RowMapping, Delete
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.dialects.postgresql import Insert

from db_models import User, Object, SecureMatrix

_log = logging.getLogger(__name__)
engine = create_async_engine('postgresql+asyncpg://postgres:post@localhost/mbks_lab1')


class Storage(ABC):
    def __init__(self) -> None:
        self._connected = False

    async def __aenter__(self) -> Self:
        await self.connect()
        return self

    async def __aexit__(
            self,
            exc_type: type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None,
    ) -> None:
        await self.close()

    @abstractmethod
    async def connect(self) -> None:
        if self._connected:
            raise RuntimeError("Storage is already connected")
        self._connected = True
        _log.debug("Connected to storage %r", self)

    @abstractmethod
    async def close(self) -> None:
        if not self._connected:
            raise RuntimeError("Storage is not connected")
        self._connected = False
        _log.debug("Closed connection to storage %r", self)

    @abstractmethod
    async def set_user(self, name: str, role: str = "Normal") -> None:
        pass

    @abstractmethod
    async def get_user(self, name: str | None, role: str | None) -> Sequence[Row | RowMapping | Any] | None:
        pass

    @abstractmethod
    async def user_exists(self, name: str) -> bool:
        pass

    @abstractmethod
    async def create_object(self, owner_id: int, name: str, uri: str) -> None:
        pass

    @abstractmethod
    async def delete_object(self, owner_id: int, name: str) -> None:
        pass

    @abstractmethod
    async def object_exists(self, name: str) -> bool:
        pass

    @abstractmethod
    async def get_object(self, name: str) -> str | None:
        pass

    @abstractmethod
    async def set_rights(self, object_id: int, owner_id: int, rights: str = "1000") -> None:
        pass

    @abstractmethod
    async def get_rights(self, object_id: int | None, owner_id: int | None) -> str | None:
        pass

class SQLAlchemyStorage(Storage):
    def __init__(self, session_factory: Callable[[], AsyncSession]) -> None:
        super().__init__()
        self._session_factory = session_factory
        self._session: AsyncSession | None = None

    async def connect(self) -> None:
        await super().connect()
        self._session = self._session_factory()
        await self._session.begin()

    async def close(self) -> None:
        await super().close()
        if self._session is None:
            raise AssertionError("Storage is not connected")
        await self._session.commit()
        await self._session.close()
        self._session = None

    async def set_user(self, name: str, role: str = "Normal") -> None:
        if self._session is None:
            raise AssertionError("Storage is not connected")
        await self._session.execute(
            Insert(User)
            .values(
                name=name,
                role=role
            )
        )

    async def get_user(self, name: str | None, role: str | None) -> Sequence[Row | RowMapping | Any] | None:
        if self._session is None:
            raise AssertionError("Storage is not connected")
        result = 0
        if name is None and role is None:
            raise AssertionError("Не заданы параметры поиска")
        elif role is None:
            result = await self._session.execute(
                select(User.id, User.name, User.role)
                .where(User.name == name)
            )
        elif name is None:
            result = await self._session.execute(
                select(User.id, User.name, User.role)
                .where(User.role == role)
            )
        else:
            result = await self._session.execute(
                select(User.id, User.name, User.role)
                .where(User.role == role and User.name == name)
            )
        return result.scalars().all()

    async def user_exists(self, name: str) -> bool:
        if self._session is None:
            raise AssertionError("Storage is not connected")
        result = await self._session.execute(
            select(User.id)
            .where(User.name == name)
        )
        return result.scalar_one_or_none() is not None

    async def create_object(self, owner_id: int, name: str, uri: str) -> None:
        if self._session is None:
            raise AssertionError("Storage is not connected")
        await self._session.execute(
            Insert(Object)
            .values(
                owner_id=owner_id,
                name=name,
                uri=uri
            )
        )

    async def delete_object(self, owner_id: int, name: str) -> None:
        if self._session is None:
            raise AssertionError("Storage is not connected")
        await self._session.execute(
            Delete(Object)
            .where(Object.owner_id == owner_id and Object.name == name)
        )

    async def get_object(self, name: str) -> str | None:
        if self._session is None:
            raise AssertionError("Storage is not connected")
        result = await self._session.execute(
            select(Object.owner_id, Object.name, Object.uri)
            .where(Object.name == name)
        )
        return result.scalar_one_or_none()

    async def object_exists(self, name: str) -> bool:
        if self._session is None:
            raise AssertionError("Storage is not connected")
        result = await self._session.execute(
            select(Object.id)
            .where(Object.name == name)
        )
        return result.scalar_one_or_none() is not None

    async def set_rights(self, object_id: int, owner_id: int, rights: str = "1000") -> None:
        if self._session is None:
            raise AssertionError("Storage is not connected")
        await self._session.execute(
            Insert(SecureMatrix)
            .values(
                object_id=object_id,
                user_id=owner_id,
                rights=rights
            )
        )

    async def get_rights(self, object_id: int | None, owner_id: int | None) -> str | None:
        if self._session is None:
            raise AssertionError("Storage is not connected")
        result = await self._session.execute(
            select(SecureMatrix.object_id, SecureMatrix.user_id, SecureMatrix.rights)
            .where(SecureMatrix.object_id == object_id and SecureMatrix.user_id == owner_id)
        )
        return result.scalar_one_or_none()
