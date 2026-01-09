from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


age_kb = [
    "1", "2", "3",
    "4", "5", "6",
    "7", "8", "9",
    "Назад  ⏪", "0", "Стереть символ ❌",
    "Сохранить ✔️",
]

data_change_map = {
    "change_age": "Возраст",
    "change_gender": "Пол",
    "change_hight": "Рост",
    "change_weight": "Вес",
    "change_gender": "Пол",
    "change_hight": "Рост",
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
    return keyboard.adjust(2).as_markup()


# Клавиатура для изменения возраста
async def change_age():
    keyboard = InlineKeyboardBuilder()
    for item in age_kb:
        if item == "Сохранить ✔️":
            keyboard.button(text=item, callback_data=f"age:save")
        elif item == "Назад  ⏪":
            keyboard.button(text=item, callback_data="change_data_user")
        elif item == "Стереть символ ❌":
            keyboard.button(text=item, callback_data="age:delete")
        else:
            keyboard.button(text=item, callback_data=f"age:{item}")
    return keyboard.adjust(3).as_markup()


# Кнопка для возврата в меню профиля
back_to_profile_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(
        text="Вернуться к профилю",
        callback_data="user_progress"
    )]
])