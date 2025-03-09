from aiogram import Dispatcher
from aiogram.types import Message
from services.database import get_all_persons
from middlewares.authorization import authorized_only


# Улучшенная функция разбиения сообщений
def split_message(text, max_length=4000):  # Берем чуть меньший лимит для безопасности
    messages = []
    while text:
        if len(text) <= max_length:
            messages.append(text)
            break
        split_index = text.rfind("\n", 0, max_length)  # Ищем последнее "\n" перед лимитом
        if split_index == -1:
            split_index = max_length  # Если нет переносов строк, обрезаем просто по лимиту
        messages.append(text[:split_index])
        text = text[split_index:].lstrip()
    return messages


@authorized_only
async def show_handler(message: Message, *args, **kwargs):
    try:
        rows = await get_all_persons()
        if not rows:
            await message.answer("В базе данных нет записей.")
            return

        response_parts = []
        current_part = "Записи в базе данных:\n\n"

        for row in rows:
            entry = (
                f"ID: {row['person_id']}, "
                f"Имя: {row['person_name']}, "
                f"Фамилия: {row['person_surname']}, "
                f"Дата: {row['person_birthdate']},\n"
                f"Описание: {row['person_description']}\n\n"
            )

            if len(current_part) + len(entry) > 4000:
                response_parts.append(current_part)
                current_part = ""  # Начинаем новый блок

            current_part += entry

        if current_part:
            response_parts.append(current_part)

        # Отправляем по частям
        for part in response_parts:
            await message.answer(part)

    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")


def register_show_handlers(dp: Dispatcher):
    dp.message.register(show_handler, lambda message: message.text == "Показать данные")
