from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


paid_subscription_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Приобрести подписку прямо сейчас")] 
], resize_keyboard=True, one_time_keyboard=True)