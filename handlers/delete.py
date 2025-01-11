from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from services.database import delete_person
from middlewares.authorization import authorized_only
from keyboards.reply import main_menu


class UserStates(StatesGroup):
    waiting_for_delete = State()

@authorized_only
async def delete_handler(message: Message, state: FSMContext, *args, **kwargs):
    await message.answer("Введите ID записи, которую хотите удалить. Если передумали введите: 'Отмена'")
    await state.set_state(UserStates.waiting_for_delete)


@authorized_only
async def process_delete_data(message: Message, state: FSMContext, *args, **kwargs):
    process = message.text.strip()
    if process == "Отмена":
        await message.answer("Действие отменено.", reply_markup=main_menu())
        await state.clear()
        return
    try:
        person_id = int(message.text)
        await delete_person(person_id)
        await message.answer(f"Запись с ID {person_id} успешно удалена.")
        await state.clear()
    except ValueError:
        await message.answer("ID должен быть числом. Попробуйте снова.")
    except Exception as e:
        await message.answer(f"Ошибка при удалении записи: {e}")
        await state.clear()


def register_delete_handlers(dp: Dispatcher):
    dp.message.register(delete_handler, lambda message: message.text == "Удалить данные")
    dp.message.register(process_delete_data, UserStates.waiting_for_delete)