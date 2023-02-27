import asyncio

from command_Interpreter import write_command
from config import storage
from user_worker import check_enter


async def login(name: str) -> None:
    if await check_enter(user=name):
        print(f"Успешная авторизация пользователя {name}")
        await write_command(user=name)
    else:
        print("Такого пользователя не существует")


def main():
    name = input("Введите имя пользователя \n")
    asyncio.run(login(name=name))


if __name__ == '__main__':
    main()
