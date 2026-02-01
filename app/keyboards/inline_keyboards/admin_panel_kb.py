from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from Database.mapping.people_to_db_map import search_user_map

from Database.mapping.people_to_db_map import *


main_menu_kb =InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(
        text="Найти пользователя по тг-айди",
        callback_data="search_user_by_tg_id",
    )],
    [InlineKeyboardButton(
        text="Отпарвить сообщение в определённый чат",
        callback_data="send_message_to_chat",
    )],
])


whom_to_send_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(
        text="Обычным пользователям",
        callback_data="common_user",
    )],
    [InlineKeyboardButton(
        text="Тренерам",
        callback_data="trainer_user",
    )],
    [InlineKeyboardButton(
        text="Определённому пользователю",
        callback_data="special_user",
    )],
    [InlineKeyboardButton(
        text="В закрытый тгк",
        callback_data="to_close_chanel",
    )],
    [InlineKeyboardButton(
        text="🏠 Вернуться в главное меню",
        callback_data="back_main_menu_admin"
    )],
])


back_main_menu_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(
        text="🏠 Вернуться в главное меню",
        callback_data="back_main_menu_admin"
    )]
])


async def search_user_menu_kb():
    keyboard = InlineKeyboardBuilder()
    for items, values in search_user_map.items():
        keyboard.add(InlineKeyboardButton(text=values, callback_data=items))
    return keyboard.adjust(2, 1).as_markup()


async def update_data_user_by_admin():
    keyboard = InlineKeyboardBuilder()
    for items, values in update_data_user_by_admin_map.items():
        keyboard.add(InlineKeyboardButton(text=values, callback_data=items))
    return keyboard.adjust(2).as_markup()


gender_change = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(
        text="Мужской ♂️",
        callback_data="new_gender:male",
    )],
    [InlineKeyboardButton(
        text="Женский ♀️",
        callback_data="new_gender:womale",
    )],
])


subscribe_change = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(
        text="Удалить подписку",
        callback_data="new_sub:delete_subscribe"
    )],
    [InlineKeyboardButton(
        text="Продлить на 1 месяц",
        callback_data="new_sub:sub_1_month"
    )],
    [InlineKeyboardButton(
        text="Продлить на 3 месяца",
        callback_data="new_sub:sub_3_month"
    )],
    [InlineKeyboardButton(
        text="Продлить на 6 месяцев",
        callback_data="new_sub:sub_6_month"
    )],
    [InlineKeyboardButton(
        text="Продлить на 1 год",
        callback_data="new_sub:sub_1_year"
    )],
])