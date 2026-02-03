import os
from dotenv import load_dotenv

from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.exceptions import TelegramAPIError, TelegramBadRequest, TelegramNetworkError, TelegramForbiddenError

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import app.keyboards.inline_keyboards.admin_panel_kb as inl_kb

import Database.requests.orm as rq_orm
import Database.requests.core as rq_core

from app.panels.admin_panel.admin_menu import main_menu_admin
from config import bot


send_message_admin_router = Router()


load_dotenv()
admins = int(os.getenv("ADMIN_ID"))
trainer = int(os.getenv("TRAINER_ID"))
tgk_id = int(os.getenv("CLOSE_TGK"))


WHO_GET_MESSAGE = {
    "common_user" : "Обычным пользователям",
    "trainer_user": "Тренерам",
    "special_user" : "Определённому пользователю",
    "to_close_chanel": "В закрытый тгк",
}


# Машина состояния для отправки сообщений
class Send_message(StatesGroup):
    who = State()
    id_user_from_tg = State()
    what = State() 


"""                  Начало отправления сообщения                  """


@send_message_admin_router.callback_query(F.data == "send_message_to_chat")
async def start_send_message(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    await state.set_state(Send_message.who)
    await callback.message.edit_text("Кому вы хотите отправить сообщение 🔎", reply_markup=inl_kb.whom_to_send_kb)


# Что отправить в сообщении
@send_message_admin_router.callback_query(Send_message.who, F.data != "special_user")
async def continue_send_message(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    who_get_message = callback.data
    who_get_message_value = WHO_GET_MESSAGE.get(who_get_message)

    await state.update_data(who=who_get_message)
    await state.set_state(Send_message.what)

    await callback.message.edit_text(f"Отлично, теперь напишите, что вы хотели бы отправить в чат: {who_get_message_value}", reply_markup=inl_kb.back_main_menu_kb)


"""                  Начало отправления сообщения конкретному пользователю                  """


@send_message_admin_router.callback_query(Send_message.who, F.data == "special_user")
async def continue_send_message_spec_user(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    who_get_message = callback.data

    await state.update_data(who=who_get_message)
    await state.set_state(Send_message.id_user_from_tg)

    await callback.message.answer("Введите tg-айди пользователя, которому Вы хотите написать", reply_markup=inl_kb.back_main_menu_kb)


@send_message_admin_router.message(Send_message.id_user_from_tg)
async def continue2_send_message_spec_user(message: Message, state: FSMContext):
    search_id = message.text
    
    if not search_id.isdigit():
        await message.answer("Пожалуйста, введите tg-айди пользователя цифрами!")
        return
    
    rq = await rq_core.AsyncCore.is_tg_id_real(tg_id=search_id) # Проверяем, есть ли такой пользователь с таким tg_id вообще
    if rq is False:
        await message.answer("Произошла ошибка! Пользователя с таким айди не существует! Повторите попытку")
        return
    
    await state.update_data(id_user_from_tg=str(message.text))
    await state.set_state(Send_message.what)

    await message.answer("Отлично, теперь напишите, что вы хотели бы отправить в чат этому пользователю:", reply_markup=inl_kb.back_main_menu_kb)


"""              ОТПРАВКА СООБЩЕНИЯ              """


@send_message_admin_router.message(Send_message.what or F.data == "send_message_to_uniq_user")
async def finish_send_message(message: Message, state: FSMContext):
    try:  
        rq = await rq_orm.AsyncOrm.information_about_user_info()
        tg_id_users = [int(items.tg_id) for items in rq] # tg_id пользователей
    
        await state.update_data(what=message.text)
        message_dict = await state.get_data()

        # Отправка сообщений в зависимости от callback'а
        if message_dict['who'] == "common_user":
            for id_users in tg_id_users:
                try:
                    await bot.send_message(
                        chat_id=id_users,
                        text=message_dict['what']
                    )
                except Exception as e:
                    print(f"Произошла неопознанная ошибка в admin_panel: {e}")
                    continue
        elif message_dict['who'] == "to_close_chanel":
            await bot.send_message(
                chat_id=tgk_id,
                text=message_dict['what'])
        elif message_dict['who'] == "trainer_user":
            await bot.send_message(
                chat_id=trainer,
                text=(
f"""
📨 СООБЩЕНИЕ ОТ АДМИНА\n
{message_dict['what']}
"""))
        elif message_dict['who'] == "special_user":
            await bot.send_message(
                chat_id=int(message_dict['id_user_from_tg']),
                text=(
f"""
📨 СООБЩЕНИЕ ОТ АДМИНА\n
{message_dict['what']}
"""))

            
        await message.answer("Ваше сообщение было успешно отправлено в чат!")
        return await main_menu_admin(message)
    
    except TelegramForbiddenError as e:
        print(f"Произошла ошибка в admin_panel, пользователь заблокировал бота: {e}")
    except TelegramNetworkError as e:
        print(f"Произошла ошибка TelegramNetworkError в admin_panel: {e}")
    except TelegramAPIError as e:
        print(f"Произошла ошибка TelegramAPIError в admin_panel: {e}")
    except  TelegramBadRequest as e:
        print(f"Произошла ошибка TelegramBadRequest в admin_panel: {e}")
    except Exception as e:
        print(f"Произошла неопознанная ошибка в admin_panel: {e}")
    finally:
        await state.clear()


# Если админ отправляет с профиля письмо 

@send_message_admin_router.message(Send_message.what or F.data == "send_message_to_uniq_user")
async def finish_send_message(message: Message, state: FSMContext):
    try:  
        rq = await rq_orm.AsyncOrm.information_about_user_info()
        tg_id_users = [int(items.tg_id) for items in rq] # tg_id пользователей
    
        await state.update_data(what=message.text)
        message_dict = await state.get_data()

        # Отправка сообщений в зависимости от callback'а
        if message_dict['who'] == "common_user":
            for id_users in tg_id_users:
                await bot.send_message(
                    chat_id=id_users,
                    text=message_dict['what']
                )
        elif message_dict['who'] == "to_close_chanel":
            await bot.send_message(
                chat_id=tgk_id,
                text=message_dict['what'])
        elif message_dict['who'] == "trainer_user":
            await bot.send_message(
                chat_id=trainer,
                text=(
f"""
📨 СООБЩЕНИЕ ОТ АДМИНА\n
{message_dict['what']}
"""))
        elif message_dict['who'] == "special_user":
            await bot.send_message(
                chat_id=int(message_dict['id_user_from_tg']),
                text=(
f"""
📨 СООБЩЕНИЕ ОТ АДМИНА\n
{message_dict['what']}
"""))

            
        await message.answer("Ваше сообщение было успешно отправлено в чат!")
        return await main_menu_admin(message)
    
    except Exception as e:
        print(f"Произошла неопознанная ошибка в admin_panel: {e}")
    except TelegramNetworkError as e:
        print(f"Произошла ошибка TelegramNetworkError в admin_panel: {e}")
    except TelegramAPIError as e:
        print(f"Произошла ошибка TelegramAPIError в admin_panel: {e}")
    except  TelegramBadRequest as e:
        print(f"Произошла ошибка TelegramBadRequest в admin_panel: {e}")
    finally:
        await state.clear()