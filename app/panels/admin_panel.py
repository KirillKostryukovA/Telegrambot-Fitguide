import os
from dotenv import load_dotenv

from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.filters import CommandStart
from aiogram.exceptions import TelegramAPIError, TelegramBadRequest, TelegramNetworkError

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import app.keyboards.inline_keyboards.admin_panel_kb as inl_kb

import Database.requests.orm as rq_orm

from config import bot


admin_panel_router = Router()


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
    what = State() 


# Главное меню в админ панеле
@admin_panel_router.message(CommandStart())
async def main_menu_admin(message: Message):
    if message.from_user.id == admins:
        await message.answer("""
    👨‍💼 АДМИН-ПАНЕЛЬ | FitGuide

    Выберите действие:
    """, reply_markup=inl_kb.main_menu_kb)
        

# Пользователь отправляет сообщения 
@admin_panel_router.callback_query(F.data == "send_message_to_chat")
async def start_send_message(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    await state.set_state(Send_message.who)
    await callback.message.edit_text("Кому вы хотите отправить сообщение 🔎", reply_markup=inl_kb.whom_to_send_kb)


# Что отправить в сообщении
@admin_panel_router.callback_query(Send_message.who, F.data != "special_user")
async def continue_send_message(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    who_get_message = callback.data
    who_get_message_value = WHO_GET_MESSAGE.get(who_get_message)

    await state.update_data(who=who_get_message)
    await state.set_state(Send_message.what)

    await callback.message.edit_text(f"Отлично, теперь напишите, что вы хотели бы отправить в чат: {who_get_message_value}")


# Отправляем сообщение
@admin_panel_router.message(Send_message.what)
async def finish_send_message(message: Message, state: FSMContext):
    try:  
        rq = await rq_orm.AsyncOrm.information_about_user_info()
        tg_id_users = [int(items.tg_id) for items in rq] # tg_id пользователей
    
        await state.update_data(what=message.text)
        message_dict = await state.get_data()

        if message_dict['who'] != "trainer_user":
            for id_users in tg_id_users:
                await bot.send_message(
                    chat_id=id_users if message_dict['who'] == "common_user" else tgk_id,
                    text=message_dict['what']
                )
        else:
            await bot.send_message(
                chat_id=trainer,
                text=message_dict['what']
            )

        await message.answer("Ваше сообщие было успешно отправлено в чат!")
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