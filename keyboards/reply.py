from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Добавить данные")],
        [KeyboardButton(text="Показать данные")],
        [KeyboardButton(text="Удалить данные")],
        [KeyboardButton(text="Показать дни рождения")],
        [KeyboardButton(text="Изменить описание")]
    ], resize_keyboard=True)

def month_keyboard():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="01"), KeyboardButton(text="02"), KeyboardButton(text="03")],
        [KeyboardButton(text="04"), KeyboardButton(text="05"), KeyboardButton(text="06")],
        [KeyboardButton(text="07"), KeyboardButton(text="08"), KeyboardButton(text="09")],
        [KeyboardButton(text="10"), KeyboardButton(text="11"), KeyboardButton(text="12")],
        [KeyboardButton(text="Отмена")]
    ], resize_keyboard=True)