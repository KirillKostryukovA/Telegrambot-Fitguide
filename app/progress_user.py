from aiogram import Router, F
from aiogram.types import Message

import Database.requests.orm as rq_orm

user_progress_router = Router()


@user_progress_router.message(F.text == "📈 Мой прогресс")
async def user_profile(message: Message):
    information = await rq_orm.AsyncOrm.information_about_user(tg_id=message.from_user.id)
    
    await message.answer(f"""
📊 Вот ваш профиль и прогресс:

Здесь собрана вся информация, на основе которой строится ваша персонализированная программа. Вы можете редактировать эти данные в любой момент.

🔹 Основные параметры:
• Возраст: {information['old']}
• Пол: {information['gender']}
• Рост: {information['hight']} см
• Вес: {information['weight']} кг

🔹 Образ жизни:
• Уровень активности: {information['activity']}
• Сон (в сутки): {information['sleep_time']} часов
• Привычки, требующие внимания: {information['bad_habbits']}
• Доп. информация и цели: {information['additional_information']}
""")