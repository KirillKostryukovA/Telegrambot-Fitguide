from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from Database.mapping.people_to_db_map import activity_map, sleep_time_map


gender_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(
        text="Мужской ♂️",
        callback_data="gender:man"
    )],
    [InlineKeyboardButton(
        text="Женский ♀️",
        callback_data="gender:woman"
    )],
],)


async def activity_kb():
    keyboard = InlineKeyboardBuilder()
    for keys, values in activity_map.items():
        keyboard.add(InlineKeyboardButton(
            text=values,
            callback_data=f"activity:{keys}"
        ))
    return keyboard.adjust(2).as_markup()


async def sleep_time_kb():
    keyboard = InlineKeyboardBuilder()
    for keys, values in sleep_time_map.items():
        keyboard.add(InlineKeyboardButton(
            text=values,
            callback_data=f"sleep_time:{keys}"
        ))
    return keyboard.adjust(2).as_markup()


bad_habbits_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(
        text="Да, у меня есть вредная привычка/зависимость",
        callback_data="bad_habbits:presence_bad_habbits"
    )],
    [InlineKeyboardButton(
        text="Нет, у меня нет вредных привычек/зависимостей",
        callback_data="bad_habbits:no_bad_habbits"
    )],
],)


update_data_survey_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(
        text="Да, обновить данные", 
        callback_data="update_data_survey"
        )],
    [InlineKeyboardButton(
        text="Нет, всё актуально",
        callback_data="back_main_menu"
    )],
],)