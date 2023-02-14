from sqlalchemy.ext.asyncio import AsyncSession

from database import Storage, SQLAlchemyStorage, engine

storage: Storage = SQLAlchemyStorage(lambda: AsyncSession(engine))


async def login(name: str) -> str:
    async with storage:
        if storage.user_exists(name=name):
            return f"Вы успешно зашли под пользователем {name}"
        else:
            return "Такого пользователя не существует"

def main():
    print('ass')


if __name__ == '__main__':
    main()
