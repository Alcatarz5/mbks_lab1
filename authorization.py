from config import storage


async def login(name: str):
    async with storage:
        if await storage.user_exists(name=name):
            print(f"Вы успешно зашли под пользователем {name}")
        else:
            raise Exception('ValueError', 'Такого пользователя не существует')
