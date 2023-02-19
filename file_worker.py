import os.path

from config import storage


async def get_rights_to_file(user: str, object_name: str) -> list:
    user_data = await storage.get_user(name=user, role=None)
    if await storage.object_exists(name=object_name):
        object_data = await storage.get_object(name=object_name)
    else:
        raise Exception("ValueError", "Такого объекта не существует")
    rights = await storage.get_rights(object_id=object_data.id, owner_id=user_data.id)
    return list(rights.rights)


async def read_file(user: str, object_name: str) -> None:
    rights = await get_rights_to_file(user=user, object_name=object_name)
    if rights[0] == '1':
        object_data = await storage.get_object(name=object_name)
        file_uri = object_data.uri
        with open(file_uri, 'r') as f:
            data = f.read()
            print(data)
    else:
        print("У вас нет прав на чтение этого файла")


async def write_to_file(user: str, object_name: str, data: str) -> None:
    rights = await get_rights_to_file(user=user, object_name=object_name)
    print(rights)
    if rights[1] == '1':
        object_data = await storage.get_object(name=object_name)
        file_uri = object_data.uri
        print(file_uri)
        with open(file_uri, "a") as f:
            f.write(data)
    else:
        print("У вас нет прав на чтение этого файла")


async def create_object(user: str, object_name: str) -> None:
    open(f"./objects/{object_name}.txt", "x")
    filepath = os.path.abspath(object_name + ".txt")
    user_id = await storage.get_user(name=user, role=None)
    # print(user_id[0])
    await storage.create_object(owner_id=int(user_id[0].id), name=object_name, uri=filepath)


async def delete_object(user: str, object_name: str) -> None:
    filepath = os.path.abspath(object_name + ".txt")
    user_id = (await storage.get_user(name=user, role=None))[0].id
    os.remove(filepath)
    await storage.delete_object(owner_id=int(user_id), name=object_name)
