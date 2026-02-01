from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


main_menu_map = {
    'survey': '📊 Пройти опрос',
    'training_prog': '🎯 Индивидуальная программа тренировок',
    'meal_plan': '🥗 Индивидуальный план питания',
    'free_training_plan': '💪 Готовые тренировки',
    'user_progress': '📈 Мой прогресс',
    'help_for_user': '❓ Помощь / FAQ',
    'buy_subscribe': '💎 Купить подписку',
    'my_subscribe': '🔐 Моя подписка'
}

# Главное меню
async def main_menu_kb():
    keyboard = InlineKeyboardBuilder()
    for items, values in main_menu_map.items():
        keyboard.add(InlineKeyboardButton(text=values, callback_data=f"{items}"))
    return keyboard.adjust(2).as_markup()