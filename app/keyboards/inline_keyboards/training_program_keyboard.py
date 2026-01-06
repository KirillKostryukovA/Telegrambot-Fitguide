from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


training_program_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(
        text="Да, хочу идеальную программу тренировок",
        callback_data="perfect_program_training"
    )],
    [InlineKeyboardButton(
        text="Нет, в следующий раз",
        callback_data="get_free_program_training"
    )],
],)