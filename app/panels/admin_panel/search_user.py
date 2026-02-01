from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import app.keyboards.inline_keyboards.admin_panel_kb as inl_kb

import Database.requests.core as rq_core
import Database.requests.orm as rq_orm

from Database.mapping.people_to_db_map import *

from config import bot


search_user_router = Router()

USER_TG_ID = None # Эта переменная будет хранить tg_id пользователя, с которым админ взаимодействует

class Search_user(StatesGroup):
    tg_id_user = State()


class EditProfileByAdmin(StatesGroup):
    field = State()
    value = State()


"""                  Поиск пользователя                  """


@search_user_router.callback_query(F.data == "search_user_by_tg_id")
async def search_user(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    await state.set_state(Search_user.tg_id_user)
    await callback.message.edit_text("Введите tg_id пользователя, которого Вы хотели бы найти:", reply_markup=inl_kb.back_main_menu_kb)


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

    global USER_TG_ID
    USER_TG_ID = user_info_dict.tg_id

    try:
        if user_info_dict.paid_subcreption == True:
            # Преобразуем значения с типом данных datetime в str
            subscription_duration_time = user_info_dict.subscription_duration.strftime('%Y-%m-%d')
    
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
    • Статус: активна до (год-месяц-день) {subscription_duration_time}

    📝 Дополнительная информация и цели:

    {user_data_dict['additional_information']}
    """, reply_markup=await inl_kb.search_user_menu_kb())
        else:
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
    • Статус: отсутствует

    📝 Дополнительная информация и цели:

    {user_data_dict['additional_information']}
    """, reply_markup=await inl_kb.search_user_menu_kb())

    except Exception as e:
        print(f"Произошла неопознанная ошибка в search_user.py: {e}")
    finally:
        await state.clear()


"""                  Редактируем профиль пользователя                  """


@search_user_router.callback_query(F.data=="change_data_user_by_admin")
async def change_data_user_by_admin1(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    await state.update_data(target_id_user=USER_TG_ID)
    
    await state.set_state(EditProfileByAdmin.field)
    await callback.message.edit_text("Что вы хотите изменить?", reply_markup=await inl_kb.update_data_user_by_admin())


@search_user_router.callback_query(EditProfileByAdmin.field)
async def change_data_user_by_admin2(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    field = callback.data
    await state.update_data(field=field)
    
    await state.set_state(EditProfileByAdmin.value)

    if field == "change_gender":
        await callback.message.edit_text("Выберите пол:", reply_markup=inl_kb.gender_change)
    elif field == "change_subscribe":
        await callback.message.edit_text("Выберите действие с подпиской:", reply_markup=inl_kb.subscribe_change)


# Изменяем значение гендера
@search_user_router.callback_query(EditProfileByAdmin.value, F.data.startswith("new_gender:"))
async def new_gender_user(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    try:
        value = callback.data.split(":")[1]

        dict_to_send = await state.get_data()

        await rq_core.AsyncCore.update_gender_by_admin(tg_id=int(dict_to_send['target_id_user']), value=value)
        
        if value == "male":
            await callback.message.edit_text(f"Значение пола пользователя с айди {dict_to_send['target_id_user']} было успешно заменено: мужской")
        else:
            await callback.message.edit_text(f"Значение пола пользователя с айди {dict_to_send['target_id_user']} было успешно заменено: женский")

    except Exception as e:
        print(f"Произошла неопознанная ошибка в search_user в функции new_gender_user: {e}")
    finally:
        await state.clear()


# Изменяем подписку пользователя
@search_user_router.callback_query(EditProfileByAdmin.value, F.data.startswith("new_sub:"))
async def new_subscribe_user(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    subs_value = callback.data.split(":")[1]
    subs_value_people_read = subscription_time_gift_map.get(subs_value)

    data_dict = await state.get_data()

    try:
        if subs_value == "delete_subscribe":
            await rq_core.AsyncCore.delete_subs_user(tg_id=int(data_dict['target_id_user']))
            await callback.message.answer(f"Подписка у пользователя с айди {data_dict['target_id_user']} была успешно удалена!", reply_markup=inl_kb.back_main_menu_kb)
        else:
            await rq_orm.AsyncOrm.update_user_paym_sub(tg_id=int(data_dict['target_id_user']), payload=subs_value)
            await callback.message.edit_text(f"Подписка у пользователя с айди {data_dict['target_id_user']} успешно продлена {subs_value_people_read}!", reply_markup=inl_kb.back_main_menu_kb)

            await bot.send_message(
                chat_id=int(data_dict['target_id_user']),
                text=
                f"""
🎉 Подписка активирована!

Вам был предоставлен доступ к премиум-функциям {subs_value_people_read}! Спасибо, что выбрали нас!

✨ Теперь вам полностью доступно:
• Персональная программа — тренировки от вашего тренера.
• Индивидуальный план питания — рацион под ваши цели.
• Закрытый ТГК — участие в комьюнити и гонка за призами.
""")
            
    except Exception as e:
        print(f"Произошла ошибка в search_user.py в new_subscribe_user: {e}")
    finally:
        await state.clear()