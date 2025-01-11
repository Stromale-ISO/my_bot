from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from services.database import add_person
from middlewares.authorization import authorized_only
from keyboards.reply import main_menu

class UserStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_surname = State()
    waiting_for_birthdate = State()
    waiting_for_description = State()




@authorized_only
async def start_add_handler(message: Message, state: FSMContext, *args, **kwargs):
    await message.answer("Введите имя:")
    await state.set_state(UserStates.waiting_for_name)

@authorized_only
async def process_name(message: Message, state: FSMContext, *args, **kwargs):
    name = message.text.strip()
    if not name.isalpha():
        await message.answer("Имя должно содержать только буквы. Попробуйте снова.")
        return
    await state.update_data(name=name)
    await message.answer("Введите фамилию:")
    await state.set_state(UserStates.waiting_for_surname)

@authorized_only
async def process_surname(message: Message, state: FSMContext, *args, **kwargs):
    surname = message.text.strip()
    if not surname.isalpha():
        await message.answer("Фамилия должна содержать только буквы. Попробуйте снова.")
        return
    await state.update_data(surname=surname)
    await message.answer("Введите дату рождения (в формате ГГГГ-ММ-ДД):")
    await state.set_state(UserStates.waiting_for_birthdate)

@authorized_only
async def process_birthdate(message: Message, state: FSMContext, *args, **kwargs):
    birthdate = message.text.strip()
    from datetime import datetime
    try:
        datetime.strptime(birthdate, "%Y-%m-%d")
    except ValueError:
        await message.answer("Неправильный формат даты. Попробуйте снова. (Пример: 2000-01-01)")
        return
    await state.update_data(birthdate=birthdate)
    await message.answer("Введите описание:")
    await state.set_state(UserStates.waiting_for_description)

@authorized_only
async def process_description(message: Message, state: FSMContext, *args, **kwargs):
    description = message.text.strip()
    if len(description) < 5:
        await message.answer("Описание должно быть длиной хотя бы 5 символов. Попробуйте снова.")
        return

    user_data = await state.get_data()
    name = user_data["name"]
    surname = user_data["surname"]
    birthdate = user_data["birthdate"]

    try:
        await add_person(name, surname, birthdate, description)
        await message.answer("Данные успешно добавлены в базу.", reply_markup=main_menu())
        await state.clear()
    except Exception as e:
        await message.answer(f"Ошибка при добавлении данных: {e}", reply_markup=main_menu())


# @authorized_only
# async def cansel_handler(message: Message, state: FSMContext, *args, **kwargs):
#     current_state = await state.get_state()
#     if current_state is None:
#         await message.answer("Нечего отменять")
#         return
#     await state.clear()
#     await message.answer("Действие отменено")


def register_add_handlers(dp: Dispatcher):
    dp.message.register(start_add_handler, lambda message: message.text == "Добавить данные")
    dp.message.register(process_name, UserStates.waiting_for_name)
    dp.message.register(process_surname, UserStates.waiting_for_surname)
    dp.message.register(process_birthdate, UserStates.waiting_for_birthdate)
    dp.message.register(process_description, UserStates.waiting_for_description)
    # dp.message.register(cansel_handler, lambda message: message.text.lower() == "отмена")