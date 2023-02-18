from config import storage


async def add_user(user: str, role: str) -> None:
    await storage.set_user(name=user, role=role)
