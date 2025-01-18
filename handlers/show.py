from aiogram import Dispatcher
from aiogram.types import Message
from services.database import get_all_persons
from middlewares.authorization import authorized_only

@authorized_only
async def show_handler(message: Message, *args, **kwargs):
    try:
        rows = await get_all_persons()
        if rows:
            response = "Записи в базе данных:\n\n"
            for row in rows:
                response += (
                    f"ID: {row['person_id']}, "
                    f"Имя: {row['person_name']}, "
                    f"Фамилия: {row['person_surname']}, "
                    f"Дата: {row['person_birthdate']},\n"
                    f"Описание: {row['person_description']}\n\n"
                )
            await message.answer(response)
        else:
            await message.answer("В базе данных нет записей.")
    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")


def register_show_handlers(dp: Dispatcher):
    dp.message.register(show_handler, lambda message: message.text == "Показать данные")