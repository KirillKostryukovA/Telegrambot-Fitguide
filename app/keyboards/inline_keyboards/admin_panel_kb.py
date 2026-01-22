from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


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
        text="Вернуться в главное менбю",
        callback_data="back_main_menu_admin"
    )],
])


back_main_menu_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(
        text="Вернуться в главное менбю",
        callback_data="back_main_menu_admin"
    )]
])