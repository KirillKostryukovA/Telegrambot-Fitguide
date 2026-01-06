from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


main_menu_map = {
    'survey': '📊 Пройти опрос',
    'training_prog': '🎯 Индивидуальная программа тренировок',
    'meal_plan': '🥗 Индивидуальный план питания',
    'free_training_plan': '💪 Готовые тренировки',
    'user_progress': '📈 Мой прогресс',
    'help_for_user': '❓ Помощь / FAQ',
}

activity_map = {
    "very_hight": "Каждый день",
    "hight": "Более 3-х раз в неделю",
    "middle": "3 раза в неделю",
    "low": "Вообще не занимаюсь",
}

sleep_time_map = {
    "very_long": "Более 10 часов",
    "long": "8-10 часов",
    "normal": "6-8 часов",
    "very_bad": "Менее 6 часов",
}

# Главное меню
async def main_menu_kb():
    keyboard = InlineKeyboardBuilder()
    for items, values in main_menu_map.items():
        keyboard.add(InlineKeyboardButton(text=values, callback_data=f"{items}"))
    return keyboard.adjust(2).as_markup()


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