from sqlalchemy.ext.asyncio import AsyncSession

from database import Storage, SQLAlchemyStorage, engine

storage: Storage = SQLAlchemyStorage(lambda: AsyncSession(engine))


async def get_rights_to_file(user: str, object_name: str) -> list:
    right_to_read = None
    async with storage:
        user_data = await storage.get_user(name=user)
        if await storage.object_exists(name=object_name):
            object_data = await storage.get_object(name=object_name)
        else:
            raise Exception("ValueError", "Такого объекта не существует")
        rights = await storage.get_rights(object_id=object_data.id, owner_id=user_data.id)
        right_to_read = rights.rights[0]
    return list(right_to_read)


async def read_file(user: str, object_name: str) -> None:
    rights = get_rights_to_file(user=user, object_name=object_name)
    if rights[0] == 1:
        file_uri = None
        async with storage:
            object_data = await storage.get_object(name=object_name)
            file_uri = object_data.uri
        data = open(file_uri, "r")
        print(data)
    else:
        print("У вас нет прав на чтение этого файла")

async def change_file(user: str, object_name: str, data: str) -> None:
    rights = get_rights_to_file(user=user, object_name=object_name)
    if rights[1] == 1:
        file_uri = None
        async with storage:
            object_data = await storage.get_object(name=object_name)
            file_uri = object_data.uri
        with open(file_uri, "w") as f:
            print(data, f)
    else:
        print("У вас нет прав на чтение этого файла")


