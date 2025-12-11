from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

main_menu_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="📊 Пройти опрос")],
    [KeyboardButton(text="💪 Готовые тренировки")],
    [KeyboardButton(text="🥗 База знаний о питании")],
    [KeyboardButton(text="📈 Мой прогресс")],
    [KeyboardButton(text="❓ Помощь / FAQ")],
], resize_keyboard=True, one_time_keyboard=True)


gender_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Мужской ♂️")], [KeyboardButton(text="Женский ♀️")],
], resize_keyboard=True, one_time_keyboard=True)


activity_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Каждый день")], [KeyboardButton(text="Более 3-х раз в неделю")],
    [KeyboardButton(text="3 раза в неделю")], [KeyboardButton(text="Вообще не занимаюсь")],
], resize_keyboard=True, one_time_keyboard=True)


sleep_time_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Более 10 часов")], [KeyboardButton(text="8-10 часов")],
    [KeyboardButton(text="6-8 часов")], [KeyboardButton(text="Менее 6 часов")], 
], resize_keyboard=True, one_time_keyboard=True)


bad_habbits_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Нет, у меня нет вредных привычек/зависимостей")],
    [KeyboardButton(text="Да, у меня есть вредная привычка/зависимость")],
], resize_keyboard=True, one_time_keyboard=True)


additional_information = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="У меня нет никаких ограничений/болезней/аллергий/т.д")]
], resize_keyboard=True, one_time_keyboard=True)


free_programs_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=("Да, хочу идеальную программу тренировок"))],
    [KeyboardButton(text=("Нет, в следующий раз"))],
], resize_keyboard=True, one_time_keyboard=True)