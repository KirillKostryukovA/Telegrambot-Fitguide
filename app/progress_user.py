from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramNetworkError, TelegramAPIError

import Database.requests.orm as rq_orm

import app.keyboards.inline_keyboards.progress_user_keyboard as inl_kb


user_progress_router = Router()


# Показываем профиль пользователя ... пользователю
@user_progress_router.callback_query(F.data == "user_progress")
async def user_profile(callback: CallbackQuery):
    await callback.answer()
    
    try:
        information = await rq_orm.AsyncOrm.information_about_user(tg_id=callback.from_user.id)
        
        await callback.message.edit_text(f"""
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
    """, reply_markup=inl_kb.user_profile_kb)
        
    except Exception as e:
        print(f"Произошла неопознанная ошибка: {e}")
    except TelegramNetworkError as e:
        print(f"Произошла ошибка сети: {e}")
    except TelegramAPIError as e:
        print(f"Произошла ошибка API Telegram: {e}")