import os
from dotenv import load_dotenv

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.exceptions import TelegramAPIError, TelegramNetworkError

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from config import bot


support_router = Router()


class Technical_support(StatesGroup):
    send_message = State()


# Пользователь пишет письмо в техподдержку
@support_router.callback_query(F.data == "help_for_user")
async def message_user_to_support(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    await callback.message.edit_text("""
🛠 Это техническая поддержка FitGuide!

Расскажите, с какой проблемой вы столкнулись. Чем подробнее вы опишете ситуацию, тем быстрее и точнее мы сможем помочь.

Чтобы ускорить решение, укажите в сообщении:

    Что произошло? (Например: «не проходит оплата», «не открывается программа»).

    Когда возникла проблема?

    Ваши действия до её появления?

    Скриншот или код ошибки (если есть).

Мы свяжемся с вами в этом чате в ближайшее время. ⏱
""")
    
    await state.set_state(Technical_support.send_message)


# Отправляем письмо в техподдержку
@support_router.message(Technical_support.send_message)
async def send_message_to_support(message: Message, state: FSMContext):
    await state.update_data(send_message=message.text)

    user_data = await state.get_data()
    user_text = user_data.get("send_message", "сообщение пустое")

    await message.answer("""
✅ Ваша заявка в поддержку принята!

Мы уже передали её специалисту. Ответ придёт в этот же чат в течение 24 часов (обычно быстрее).
""")

    try:
        load_dotenv()
        TECHNICAL_SUPPORT_ID = int(os.getenv("TECHNICAL_SUPPORT_ID"))

        await bot.send_message(
            chat_id=TECHNICAL_SUPPORT_ID, 
            text=f"""
Поступило уведомление от пользователя @{message.from_user.username}:

{user_text}
""")
        await state.clear()

    except Exception as e:
        print(f"Произошла неопознанная ошибка: {e}")
    except TelegramNetworkError as e:
        print(f"Произошла ошибка сети Telegram: {e}")
    except TelegramAPIError as e:
        print(f"Произошла ошибка API Telegram: {e}")