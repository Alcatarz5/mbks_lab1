import asyncio

from command_Interpreter import write_command
from config import storage


async def login(name: str) -> None:
    async with storage:
        if await storage.user_exists(name=name):
            print(f"Вы успешно зашли под пользователем {name}")
            await write_command(user=name)
        else:
            print("Такого пользователя не существует")


def main():
    name = input("Введите имя пользователя \n")
    asyncio.run(login(name=name))


if __name__ == '__main__':
    main()
