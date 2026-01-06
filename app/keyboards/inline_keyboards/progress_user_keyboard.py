from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


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