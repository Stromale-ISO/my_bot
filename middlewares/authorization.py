from aiogram.types import Message
from config import AUTHORIZED_USERS

def authorized_only(func):
    async def wrapper(message: Message, *args, **kwargs):
        if message.from_user.id not in AUTHORIZED_USERS:
            await message.answer("Пошел нахуй отсюда")
            return
        return await func(message, *args, **kwargs)
    return wrapper
