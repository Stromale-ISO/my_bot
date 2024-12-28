from aiogram import Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from keyboards.reply import main_menu
from middlewares.authorization import authorized_only


@authorized_only
async def start_handler(message: Message, *args, **kwargs):
    await message.answer(
        "Привет! Вот что я могу:\n"
        "1. Добавить данные\n"
        "2. Удалить данные\n"
        "3. Просмотреть данные",
        reply_markup=main_menu()
    )


def register_start_handlers(dp: Dispatcher):
    dp.message.register(start_handler, Command(commands=["start"]))