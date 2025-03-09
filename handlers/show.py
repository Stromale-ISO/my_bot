from aiogram import Dispatcher
from aiogram.types import Message
from services.database import get_all_persons
from middlewares.authorization import authorized_only

#Функция для разбивки длинного текста на части
def split_message(text, max_length=4096):
    messages = []
    while len(text) > max_length:
        split_index = text.rfind("\n", 0, max_length)  #Ищем последнее "\n" перед лимитом
        if split_index == -1:
            split_index = max_length  #Если нет переносов строк, просто обрезаем
        messages.append(text[:split_index])
        text = text[split_index:].lstrip()
    messages.append(text)  #Добавляем оставшийся кусок
    return messages

@authorized_only
async def show_handler(message: Message, *args, **kwargs):
    try:
        rows = await get_all_persons()
        if not rows:
            await message.answer("В базе данных нет записей.")
            return

        response = "Записи в базе данных:\n\n"
        for row in rows:
            response += (
                f"ID: {row['person_id']}, "
                f"Имя: {row['person_name']}, "
                f"Фамилия: {row['person_surname']}, "
                f"Дата: {row['person_birthdate']},\n"
                f"Описание: {row['person_description']}\n\n"
            )

        # Разбиваем и отправляем по частям
        messages = split_message(response)
        for part in messages:
            await message.answer(part)

    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")

def register_show_handlers(dp: Dispatcher):
    dp.message.register(show_handler, lambda message: message.text == "Показать данные")