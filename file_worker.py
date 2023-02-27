import os.path

from config import storage


async def get_rights_to_file(user: str, object_name: str) -> list:
    async with storage:
        user_data = (await storage.get_user(name=user, role=None))[0].id
        if await storage.object_exists(name=object_name):
            object_data = await storage.get_object(name=object_name, object_id=None)
        else:
            raise Exception("ValueError", "Такого объекта не существует")
        rights = await storage.get_rights(object_id=object_data.id, owner_id=user_data)
        return list(rights[0].rights)


async def read_file(user: str, object_name: str) -> None:
    rights = await get_rights_to_file(user=user, object_name=object_name)
    async with storage:
        if rights[0] == '1':
            object_data = await storage.get_object(name=object_name, object_id=None)
            file_uri = object_data.uri
            with open(file_uri, 'r') as f:
                data = f.read()
                print(f"Успешное чтение файла {object_name}")
                print(data)
        else:
            print("У вас нет прав на чтение этого файла")


async def write_to_file(user: str, object_name: str, data: str) -> None:
    rights = await get_rights_to_file(user=user, object_name=object_name)
    async with storage:
        # print(rights)
        if rights[1] == '1':
            object_data = await storage.get_object(name=object_name, object_id=None)
            file_uri = object_data.uri
            # print(file_uri)
            with open(file_uri, "a") as f:
                f.write(data)
            print(f"Файл {object_name} успешно изменен")
        else:
            print("У вас нет прав на чтение этого файла")


async def create_object(user: str, object_name: str) -> None:
    open(f"./objects/{object_name}.txt", "x")
    filepath = os.path.abspath(object_name + ".txt")
    async with storage:
        user_id = await storage.get_user(name=user, role=None)
        # print(user_id[0])
        await storage.create_object(owner_id=int(user_id[0].id), name=object_name, uri=filepath)
        print(f"спешное создание объекта {object_name} по пути <{filepath}>")


async def delete_object(user: str, object_name: str) -> None:
    filepath = os.path.abspath("./objects/" + object_name + ".txt")
    print(filepath)
    async with storage:
        user_id = (await storage.get_user(name=user, role=None))[0].id
        os.remove(filepath)
        await storage.delete_object(owner_id=int(user_id), name=object_name)
        print(f"Успешно удален объект {object_name}")


async def grand_rights(user: str, target_user: str, object_name: str, rights: str) -> None:
    async with storage:
        if await storage.user_exists(name=target_user):
            object_id = (await storage.get_object(name=object_name, object_id=None)).id
            user_id = (await storage.get_user(name=user, role=None))[0].id
            target_user_id = (await storage.get_user(name=target_user, role=None))[0].id
            user_rights = (await storage.get_rights(object_id=object_id, owner_id=user_id))[0].rights
            if user_rights[2] == '1':
                if rights[3] == '0':
                    await storage.set_rights(object_id=object_id, user_id=target_user_id, rights=rights)
                    print(f"Вы успешно изменили права пользователя {target_user}, на объект {object_name}")
                else:
                    await storage.set_rights(object_id=object_id, user_id=target_user_id, rights=rights)
                    await storage.set_rights(object_id=object_id, user_id=user_id, rights='1110')
                    await storage.update_object(name=object_name, owner_id=target_user_id)
                    print(f"Вы успешно передали права собственности на объект {object_name} пользователю {target_user}")



async def get_rights(user: str) -> None:
    async with storage:
        user_id = (await storage.get_user(name=user, role=None))[0].id
        objects_list = await storage.get_rights(object_id=None, owner_id=user_id)
        print("Ваши права на объекты в системе:")
        for cur_object in objects_list:
            object_name = (await storage.get_object(name=None, object_id=cur_object.object_id)).name
            rights = cur_object.rights
            print(f"\t {object_name} : r={rights[0]}, w={rights[1]}, tg={rights[2]}, own={rights[3]}")
