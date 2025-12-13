from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


purchasing_ps_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(
        text="1 месяц — 399 ₽",
        callback_data="button_1",
    )],
    [InlineKeyboardButton(
        text="3 месяца — 699 ₽",
        callback_data="button_2",
    )],
    [InlineKeyboardButton(
        text="6 месяцев — 999 ₽",
        callback_data="button_3",
    )],
    [InlineKeyboardButton(
        text="1 год — 1 700 ₽",
        callback_data="button_4",
    )],
],)