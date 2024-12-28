from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Добавить данные")],
        [KeyboardButton(text="Показать данные")],
        [KeyboardButton(text="Удалить данные")]
    ], resize_keyboard=True)