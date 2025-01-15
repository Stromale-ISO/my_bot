from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from services.database import update_description, check_person_exists
from middlewares.authorization import authorized_only
from keyboards.reply import main_menu


class UpdateDescriptionStates(StatesGroup):
    waiting_for_id = State()
    waiting_for_description = State()


@authorized_only
async def update_description_handler(message: Message, state: FSMContext, *args, **kwargs):
    await message.answer("Введите ID пользователя, для которого нужно обновить описание. Если вы передумали введите 'Отмена'.", reply_markup=None)
    await state.set_state(UpdateDescriptionStates.waiting_for_id)


@authorized_only
async def process_id(message: Message, state: FSMContext, *args, **kwargs):
    person_id = message.text.strip()

    if person_id.lower() == "отмена":
        await message.answer("Действие отменено.", reply_markup=main_menu())
        await state.clear()
        return

    if not person_id.isdigit():
        await message.answer("ID должен быть числом. Попробуйте снова или введите 'Отмена'")
        return

    person_id = int(person_id)


    if not await check_person_exists(person_id):
        await message.answer(f"Запись с ID {person_id} не найдена. Попробуйте снова.")
        return

    await state.update_data(person_id=person_id)
    await message.answer("Введите новое описание:")
    await state.set_state(UpdateDescriptionStates.waiting_for_description)


@authorized_only
async def process_description(message: Message, state: FSMContext, *args, **kwargs):
    new_description = message.text.strip()
    if len(new_description) < 5:
        await message.answer("Описание должно быть длиной хотя бы 5 символов. Попробуйте снова.")
        return

    data = await state.get_data()
    person_id = data["person_id"]

    try:
        await update_description(person_id, new_description)
        await message.answer("Описание успешно обновлено.", reply_markup=main_menu())
    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")
    finally:
        await state.clear()


def register_update_description_handlers(dp: Dispatcher):
    dp.message.register(update_description_handler, lambda message: message.text == "Изменить описание")
    dp.message.register(process_id, UpdateDescriptionStates.waiting_for_id)
    dp.message.register(process_description, UpdateDescriptionStates.waiting_for_description)
