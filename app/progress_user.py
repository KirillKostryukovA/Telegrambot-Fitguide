from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramNetworkError, TelegramAPIError

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import Database.requests.orm as rq_orm
import Database.requests.core as rq_core

import app.keyboards.inline_keyboards.progress_user_keyboard as inl_kb

import Database.requests.orm as rq_orm


user_progress_router = Router()


class EditProfile(StatesGroup):
    age = State()


# Показываем профиль пользователя ... пользователю
@user_progress_router.callback_query(F.data == "user_progress")
async def user_profile(callback: CallbackQuery):
    await callback.answer()
    
    try:
        information = await rq_orm.AsyncOrm.information_about_user(tg_id=callback.from_user.id)
        
        await callback.message.edit_text(f"""
    📊 Вот ваш профиль и прогресс:

Здесь собрана вся информация, на основе которой строится ваша персонализированная программа. Вы можете редактировать эти данные в любой момент.

    🔹 <b>Основные параметры:</b>
                                         
    • Возраст: {information['age']}
    • Пол: {information['gender']}
    • Рост: {information['hight']} см
    • Вес: {information['weight']} кг

    🔹 <b>Образ жизни:</b>

    • Уровень активности: {information['activity']}
    • Сон (в сутки): {information['sleep_time']} часов
    • Привычки, требующие внимания: {information['bad_habbits']}
    • Доп. информация и цели: {information['additional_information']}
    """, reply_markup=inl_kb.user_profile_kb, parse_mode='html')
        
    except Exception as e:
        print(f"Произошла неопознанная ошибка в progress_user.py: {e}")
    except TelegramNetworkError as e:
        print(f"Произошла ошибка сети в progress_user.py: {e}")
    except TelegramAPIError as e:
        print(f"Произошла ошибка API Telegram в progress_user.py: {e}")


# Пользователь хочет поменять данные о себе
@user_progress_router.callback_query(F.data == "change_data_user")
async def change_information(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Выбери категорию, которую ты хотел бы изменить:", reply_markup=await inl_kb.change_data())


# Изменить возраст 
@user_progress_router.callback_query(F.data == "change_age")
async def change_age_func(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    await state.set_state(EditProfile.age)
    await state.update_data("") 

    await callback.message.edit_text("Введите Ваш возраст:", reply_markup=await inl_kb.change_age())


# Клавиатура, оторбражающая введённый возраст
@user_progress_router.callback_query(EditProfile.age, F.data.startswith("age:"))
async def change_age_func2(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    data = await state.get_data()
    old_age = data.get("age", "")

    current_age = old_age

    action = callback.data.split(":")[1] # То, что поступило с callback

    # Если число:
    if action.isdigit():
        if len(current_age) >= 3:
            await callback.answer("Введён некорректный возраст", show_alert=True)
            return 
        
        current_age += action 
        await state.update_data(age=current_age)
   
    # Если нажато "Сохранить"
    elif action == "save":
        if not current_age or current_age=="0":
            await callback.answer("Введите возраст", show_alert=True)
            return

        await rq_core.AsyncCore.update_age_in_profile(tg_id=callback.from_user.id, age_user=int(current_age))
        await state.clear()

        await callback.message.edit_text(f"Возраст обновлён: {current_age}", reply_markup=inl_kb.back_to_profile_kb)
        return 
    
    # Если пользователь нажал на кнопку стереть
    elif action == "delete":
        if not current_age or current_age == "0":
            return 

        current_age = current_age[:-1]
        await state.update_data(age=current_age)
    
    # Проверяем, изменил ли пользователь свой возраст
    if current_age == old_age:
        return # НИЧЕГО НЕ МЕНЯЕМ 

    # Показываем введённый возраст на экране
    await callback.message.edit_text(
        f"Введите ваш возраст:\n\n<b>{current_age}</b>",
        reply_markup=await inl_kb.change_age(), parse_mode="html"
    )