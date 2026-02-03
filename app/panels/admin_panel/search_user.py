import os
from datetime import *
from dotenv import load_dotenv

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


load_dotenv()
URL_CLOSE_TGK = os.getenv("CLOSE_TGK")


now = datetime.now(timezone.utc)
DESTROYER_URL = timedelta(minutes=5)

class Search_user(StatesGroup):
    tg_id_user = State()


class EditProfileByAdmin(StatesGroup):
    field = State()
    value = State()


class Send_message_to_uniq_user(StatesGroup):
    message = State()


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

    await state.update_data(target_id_user=tg_id_user)
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


"""                  Редактируем профиль пользователя                  """


@search_user_router.callback_query(F.data=="change_data_user_by_admin")
async def change_data_user_by_admin1(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
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
        dict_data = await state.get_data()

        await rq_core.AsyncCore.update_gender_by_admin(tg_id=int(dict_data['target_id_user']), value=value)
        
        if value == "male":
            await callback.message.edit_text(f"Значение пола пользователя с айди {dict_data['target_id_user']} было успешно заменено: мужской", reply_markup=inl_kb.back_main_menu_kb)
        else:
            await callback.message.edit_text(f"Значение пола пользователя с айди {dict_data['target_id_user']} было успешно заменено: женский", reply_markup=inl_kb.back_main_menu_kb)

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
            await callback.message.edit_text(f"Подписка у пользователя с айди {data_dict['target_id_user']} была успешно удалена!", reply_markup=inl_kb.back_main_menu_kb)
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


"""                  Отправка сообщений пользователю                  """


@search_user_router.callback_query(F.data == "send_message_to_uniq_user")
async def send_message_from_adm(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    await state.set_state(Send_message_to_uniq_user.message)
    await callback.message.edit_text("Отлично, теперь напишите сообщение для пользователя:", reply_markup=inl_kb.back_main_menu_kb)


@search_user_router.message(Send_message_to_uniq_user.message)
async def send_message_from_adm2(message: Message, state: FSMContext):
    try:
        await state.update_data(message=message.text)
        data_dict = await state.get_data()

        await message.answer(f"Ваше сообщение было успешно доставлено пользователю с tg_id: {data_dict['target_id_user']}")
        await bot.send_message(
            chat_id=data_dict['target_id_user'],
            text=f"""
    📨 СООБЩЕНИЕ ОТ АДМИНА\n
    {data_dict['message']}
    """)
        
    except Exception as e:
        print(f"Произошла ошибка в search_user.py в send_message_from_adm2: {e}")
    finally:
        await state.clear()


@search_user_router.callback_query(F.data == "give_url_to_close_tgk")
async def give_url_to_close_tgk(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    data_dict = await state.get_data()

    try:
        invite = await bot.create_chat_invite_link(
            chat_id=URL_CLOSE_TGK,
            member_limit=1,
            expire_date=now + DESTROYER_URL
        )

        await callback.message.answer("Ссылка на закрытый ТГК была успешна отправлена пользователю!")
        
        await bot.send_message(
            chat_id=data_dict['target_id_user'],
            text=f"""
🔒 Ваша персональная ссылка:\n{invite.invite_link}\n
⚠️ Ссылка одноразовая и действует 5 минут"
""") 
    except Exception as e:
        print(f"Произошла неопознаянная ошибка в search_user.py в give_url_to_close_tgk: {e}")
    finally:
        await state.clear()