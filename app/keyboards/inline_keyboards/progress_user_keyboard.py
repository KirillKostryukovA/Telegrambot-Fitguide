from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from Database.mapping.people_to_db_map import activity_map, sleep_time_map


age_kb = [
    "1", "2", "3",
    "4", "5", "6",
    "7", "8", "9",
    "Назад  ⏪", "0", "Стереть символ ❌",
    "Сохранить ✔️",
]

data_change_map = {
    "change_age": "Возраст",
    "change_hight": "Рост",
    "change_weight": "Вес",
    "change_activity": "Активность",
    "change_sleep_time": "Время сна",
    "change_additional_information": "Дополнительная информация",
    "user_progress": "Назад  ⏪",
}

user_profile_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(
        text="Изменить данные",
        callback_data="change_data_user"
    )],
    [InlineKeyboardButton(
        text="Вернуться в главное меню",
        callback_data="back_main_menu"
    )],
],)


# Клавиатура выбора изменения каких-либо данных
async def change_data():
    keyboard = InlineKeyboardBuilder()
    for items, values in data_change_map.items():
        keyboard.add(InlineKeyboardButton(text=values, callback_data=items))
    return keyboard.adjust(2, 2, 2, 1).as_markup()


# Клавиатура для изменения возраста, роста, веса
async def change_data_from_kb():
    keyboard = InlineKeyboardBuilder()
    for item in age_kb:
        if item == "Сохранить ✔️":
            keyboard.button(text=item, callback_data=f"save")
        elif item == "Назад  ⏪":
            keyboard.button(text=item, callback_data="change_data_user")
        elif item == "Стереть символ ❌":
            keyboard.button(text=item, callback_data="delete")
        else:
            keyboard.button(text=item, callback_data=f"{item}")
    return keyboard.adjust(3).as_markup()


# Клавиатура для изменения активности
async def change_activity_kb():
    keyboard = InlineKeyboardBuilder()
    for keys, values in activity_map.items():
        keyboard.button(text=values, callback_data=f"activity:{keys}")
    keyboard.add(InlineKeyboardButton(text="Назад  ⏪", callback_data="user_progress"))
    return keyboard.adjust(2).as_markup()


# Клавиатура для изменения времени сна
async def change_sleep_time_kb():
    keyboard = InlineKeyboardBuilder()
    for keys, values in sleep_time_map.items():
        keyboard.add(InlineKeyboardButton(text=values, callback_data=f"sleep_time:{keys}"))
    keyboard.add(InlineKeyboardButton(text="Назад  ⏪", callback_data="user_progress"))
    return keyboard.adjust(2).as_markup()


# Кнопка для возврата в меню профиля
back_to_profile_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(
        text="Вернуться к профилю",
        callback_data="user_progress"
    )]
])