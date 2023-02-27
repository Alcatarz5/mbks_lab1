from config import storage


async def add_user(user: str, role: str) -> None:
    async with storage:
        await storage.set_user(name=user, role=role)
        print(f"Пользователь {user} успешно создан")


async def check_enter(user: str) -> bool:
    async with storage:
        is_exists = await storage.user_exists(name=user)
        return is_exists
