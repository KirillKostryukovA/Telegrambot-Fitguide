from datetime import datetime

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import app.keyboards.inline_keyboards.admin_panel_kb as inl_kb

import Database.requests.core as rq_core
import Database.requests.orm as rq_orm


search_user_router = Router()


class Search_user(StatesGroup):
    tg_id_user = State()


"""                  Поиск пользователя                  """


@search_user_router.callback_query(F.data == "search_user_by_tg_id")
async def search_user(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    await state.set_state(Search_user.tg_id_user)
    await callback.message.edit_text("Введите tg_id пользователя, которого Вы хотели бы найти:")


@search_user_router.message(Search_user.tg_id_user)
async def user_modif(message: Message, state: FSMContext):
    text_user = message.text

    if not text_user.isdigit():
        await message.answer("Напишите айди числом!")
        return
    
    is_real_id = await rq_core.AsyncCore.is_tg_id_real(tg_id=text_user) # Проверяем, есть ли такой айди в БД
    if is_real_id == False:
        await message.answer("Произошла ошибка! Такого айди не существует! Попробуйте снова")
        return
    
    tg_id_user = int(text_user) # Тг-Айди пользователя, которого ищем
    
    # Информация о пользователе
    user_info_dict = await rq_orm.AsyncOrm.information_about_user_info_one(tg_id=tg_id_user)
    user_data_dict = await rq_orm.AsyncOrm.information_about_user(tg_id=tg_id_user)

    # Преобразуем значения с типом данных datetime в str
    subscription_duration_time = user_info_dict.subscription_duration.strftime('%Y-%m-%d')
    
    try:
        await message.answer(f"""
✅ ПОЛЬЗОВАТЕЛЬ НАЙДЕН | ID: {user_info_dict.tg_id}

👤 Основная информация:
• Возраст: {user_data_dict['age']}
• Пол: {user_data_dict['gender']}
• Рост: {user_data_dict['hight']} см
• Вес: {user_data_dict['weight']} кг

📊 Статистика и активность:
• Уровень активности: {user_data_dict['activity']}
• Режим сна: {user_data_dict['sleep_time']} ч/сутки
• Вредные привычки: {user_data_dict['bad_habbits']}
• Дата регистрации (год-месяц-день): {user_data_dict['created_at']}

💰 Статус подписки:
• Статус: {user_info_dict.paid_subcreption} (активна до (год-месяц-день) {subscription_duration_time})

📝 Дополнительная информация и цели:

{user_data_dict['additional_information']}
""")
        
    except Exception as e:
        print(f"Произошла неопознанная ошибка в search_user.py: {e}")
    finally:
        await state.clear()