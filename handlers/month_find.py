from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from services.database import get_persons_by_month
from middlewares.authorization import authorized_only
from keyboards.reply import month_keyboard
from keyboards.reply import main_menu


class BirthdayStates(StatesGroup):
    waiting_for_month = State()


@authorized_only
async def birthday_search_handler(message: Message, state: FSMContext, *args, **kwargs):
    await message.answer("Выберите месяц для поиска дней рождения:", reply_markup=month_keyboard())
    await state.set_state(BirthdayStates.waiting_for_month)


@authorized_only
async def process_month_selection(message: Message, state: FSMContext, *args, **kwargs):
    month = message.text.strip()
    if month == "Отмена":
        await message.answer("Действие отменено.", reply_markup=main_menu())
        await state.clear()
        return

    if month.isdigit() and 1 <= int(month) <= 12:
        try:
            rows = await get_persons_by_month(month)
            if rows:
                response = f"Дни рождения в месяце {month}:\n\n"
                for row in rows:
                    response += (
                        f"ID: {row['person_id']}, "
                        f"Имя: {row['person_name']}, "
                        f"Фамилия: {row['person_surname']}, "
                        f"Дата: {row['person_birthdate']},\n"
                        f"Описание: {row['person_description']}\n\n"
                    )
                await message.answer(response, reply_markup=main_menu())
            else:
                await message.answer(f"В месяце {month} нет записей.", reply_markup=main_menu())
        except Exception as e:
            await message.answer(f"Произошла ошибка: {e}")
    else:
        await message.answer("Некорректный ввод. Пожалуйста, выберите месяц кнопкой на клавиатуре.")
        return
    await state.clear()


def register_birthday_handlers(dp: Dispatcher):
    dp.message.register(birthday_search_handler, lambda message: message.text == "Показать дни рождения")
    dp.message.register(process_month_selection, BirthdayStates.waiting_for_month)
