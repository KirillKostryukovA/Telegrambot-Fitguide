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

# Машина состояний
class EditProfile(StatesGroup):
    change_data = State()


# Создаём конфигурацию для изменения тех данных, для которых требуется клавиатура
EDIT_DATA_CONFIGURATION = {
    "age": {
        "name": "возраст",
        "max_length": 3,
        "min_value": 10,
        "max_value": 80,
        "unit": "лет",
        "request_update": rq_core.AsyncCore.update_age_in_profile,
        "db_field": "age"
    },
    "hight": {
        "name": "рост",
        "max_length": 3,
        "min_value": 150,
        "max_value": 250,
        "unit": "см",
        "request_update": rq_core.AsyncCore.update_hight_in_profile,
        "db_field": "hight",
    },
    "weight": {
        "name": "вес",
        "max_length": 3,
        "min_value": 40,
        "max_value": 500,
        "unit": "кг",
        "request_update": rq_core.AsyncCore.update_weight_in_profile,
        "db_field": "weight",
    },
}


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


# Возраст
@user_progress_router.callback_query(F.data == "change_age")
async def start_change_age(callback: CallbackQuery, state: FSMContext):
    await start_edit_field(callback, state, "age")
    

# Рост 
@user_progress_router.callback_query(F.data == "change_hight")
async def start_change_age(callback: CallbackQuery, state: FSMContext):
    await start_edit_field(callback, state, "hight")


# Возраст
@user_progress_router.callback_query(F.data == "change_weight")
async def start_change_age(callback: CallbackQuery, state: FSMContext):
    await start_edit_field(callback, state, "weight")


#     -----    Начало редактирования     -----  


# Данные, которые редактируются с помощью клавиатуры: возраст, рост, вес
async def start_edit_field(callback: CallbackQuery, state: FSMContext, field_type: str):
    await callback.answer()

    config_dict = EDIT_DATA_CONFIGURATION[field_type]

    await state.set_state(EditProfile.change_data)
    await state.update_data(
        field_type=field_type,
        current_data=""
    )

    await callback.message.edit_text(
        f"Введите значение {config_dict['name']}:", reply_markup=await inl_kb.change_data_from_kb() 
    )


# Клавиатура, оторбражающая введённый возраст
@user_progress_router.callback_query(EditProfile.change_data)
async def finish_edit_field(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    field_type = data.get("field_type")
    current_data = data.get("current_data")

    config_dict = EDIT_DATA_CONFIGURATION[field_type]
    action = callback.data

    # Если число:
    if action.isdigit():
        if len(current_data) >= config_dict['max_length']:
            await callback.answer("Введено некорректное значение", show_alert=True)
            return 
        
        current_data += action 
        await state.update_data(current_data=current_data)
   
    # Если нажато "Сохранить"
    elif action == "save":
        if current_data=="":
            await callback.answer("Введите корректное значение", show_alert=True)
            return
    
        if int(current_data) > config_dict['max_value'] or int(current_data) < config_dict['min_value']:
            await callback.answer("Введите корректное значение", show_alert=True)
            return

        # Блок, с помощью которого конкретная характеристика сохраняется в БД
        if config_dict['db_field'] == "age":
            await rq_core.AsyncCore.update_age_in_profile(tg_id=callback.from_user.id, age_user=int(current_data))
            await callback.message.edit_text(f"Возраст обновлён: {current_data}", reply_markup=inl_kb.back_to_profile_kb)
            return 
        elif config_dict['db_field'] == "hight":
            await rq_core.AsyncCore.update_hight_in_profile(tg_id=callback.from_user.id, hight_user=int(current_data))
            await callback.message.edit_text(f"Рост обновлён: {current_data}", reply_markup=inl_kb.back_to_profile_kb)
            return 
        elif config_dict['db_field'] == "weight":
            await rq_core.AsyncCore.update_weight_in_profile(tg_id=callback.from_user.id, weight_user=int(current_data))
            await callback.message.edit_text(f"Вес обновлён: {current_data}", reply_markup=inl_kb.back_to_profile_kb)
            return 
        
        await state.clear()

    # Если пользователь нажал на кнопку стереть
    elif action == "delete":
        if not current_data or current_data == "0":
            return 

        current_data = current_data[:-1]
        await state.update_data(current_data=current_data)

    # Показываем введённый возраст на экране
    await callback.message.edit_text(
        f"Введите значение {config_dict['name']}:\n\n<b>{current_data}</b>",
        reply_markup=await inl_kb.change_data_from_kb(), parse_mode="html"
    )
    await callback.answer()