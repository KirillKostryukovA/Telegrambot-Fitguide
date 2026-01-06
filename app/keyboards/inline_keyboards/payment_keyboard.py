from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


# Спрашиваем пользователя о приобритении подписки
paid_subscription_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(
        text="Приобрести подписку прямо сейчас",
        callback_data="buy_subscribe_now",
    )],
    [InlineKeyboardButton(
        text="Приобрести позже",
        callback_data="back_main_menu",
    )],
])


# Кнопки выбора определённой подписки
purchasing_ps_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(
        text="1 месяц — 399 ₽",
        callback_data="sub_1_month",
    )],
    [InlineKeyboardButton(
        text="3 месяца — 699 ₽",
        callback_data="sub_3_month",
    )],
    [InlineKeyboardButton(
        text="6 месяцев — 999 ₽",
        callback_data="sub_6_month",
    )],
    [InlineKeyboardButton(
        text="1 год — 1 700 ₽",
        callback_data="sub_1_year",
    )],
],)