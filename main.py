import asyncio
from bot_instance import dp, bot
from services.database import create_db_pool
from handlers.start import register_start_handlers
from handlers.add import register_add_handlers
from handlers.delete import register_delete_handlers
from handlers.show import register_show_handlers
from handlers.month_find import register_birthday_handlers
from handlers.update_description import register_update_description_handlers

async def main():
    print("Бот запущен!")
    await create_db_pool()

    register_start_handlers(dp)
    register_add_handlers(dp)
    register_delete_handlers(dp)
    register_show_handlers(dp)
    register_birthday_handlers(dp)
    register_update_description_handlers(dp)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())