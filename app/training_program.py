import os
from dotenv import load_dotenv

from aiogram import Router, F
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.exceptions import TelegramNetworkError

from app.payments import paid_subscription
from app.panels.user_panel import main_menu

import app.keyboards.inline_keyboards.training_program_keyboard as inl_kb
import app.keyboards.inline_keyboards.main_menu_keyboard as main_kb

import Database.requests.orm as rq_orm

from config import bot


program_training_router = Router()

load_dotenv()
TRAINER_ID = int(os.getenv("TRAINER_ID"))


# Бесплатная программа тренировок
@program_training_router.callback_query(F.data == "free_training_plan")
async def free_program_training(callback: CallbackQuery):
    await callback.message.edit_text("""
Супер! Ваша бесплатная программа тренировок уже ждёт. Она универсальна, и вы сможете её настроить.

Однако! Если вы хотите получить программу, которая будет учитывать ваш пол, возраст, доступный инвентарь, цели и состояние здоровья — пройдите быстрый опрос. Мы literally подстроим её под вас, и вам не придётся гадать, что делать.

Потратить 2 минуты сейчас, чтобы получить идеальную программу?
""", reply_markup=inl_kb.training_program_kb)
    

# Отправляем пользователю файл с бесплатной программой тренировок
@program_training_router.callback_query(F.data == "get_free_program_training")
async def post_free_program(callback: CallbackQuery):
    await callback.answer()
    
    await callback.message.edit_text("""
Хорошо, держи файл с универсальной программой тренировок для всех! 🏋️‍♀️

В нём есть отличная база, с которой можно начать.

А если захочешь программу, которая будет учитывать твои цели, твой уровень, твой график и здоровье — просто напиши мне, и мы сделаем её персональной под тебя.

Удачи на тренировках! 
""", reply_markup=main_kb.back_main_menu)

    try:
        load_dotenv()
        FREE_PROGRAM=os.getenv("FREE_PROGRAM")
        file_path = FREE_PROGRAM

        # Нужно отправлять файл в бинарном виде, т.к. Aiogram требует файл как BufferedReader
        file = FSInputFile(file_path)
        await callback.message.reply_document(file) 

    except Exception as e:
        print(f"Произошла неопознанная ошибка: {e}")
    except TelegramNetworkError as e:
        print(f"Произошла ошибка сети Telegram: {e}")


# Индивидуальная программа тренировок для пользователя, оплатившего подписку
@program_training_router.callback_query(F.data == "training_prog")
@program_training_router.callback_query(F.data == "perfect_program_training")
async def get_paid_training_program(callback: CallbackQuery):
    try:
        await callback.answer()
        
        is_paid = await rq_orm.AsyncOrm.verification_sub(tg_id=callback.from_user.id)
        is_data_survey = await rq_orm.AsyncOrm.verification_data_survey(tg_id=callback.from_user.id)

        if is_paid is False:
            return await paid_subscription(callback)
        elif is_data_survey is False:
            await callback.message.answer("Для того, чтобы мы могли отправить Вам индивидуальную программу тренировок, пройдите опрос")
            return await main_menu(callback)
        

        await callback.message.edit_text("""
    ✅ Отлично! Ваши данные с опроса отправлены нашему тренеру.

    Он внимательно изучит ваши ответы и в ближайшие 24 часа подготовит вашу персональную программу тренировок. Вы получите её прямо здесь, в этом чате.

    А пока предлагаем не терять время:

    🔥 Переходите в наш закрытый Telegram-канал — там уже кипит жизнь! Вы можете:
    • Познакомиться с участниками марафона
    • Узнать полезные фитнес-лайфхаки
    • Начать погружаться в атмосферу поддержки и мотивации

    Перейти в закрытый ТГ-канал

    Оставайтесь на связи! Если у вас срочный вопрос, вы всегда можете написать нам.
    """, reply_markup=main_kb.back_main_menu)
        
        await send_message_trainer(callback)
    
    except TelegramNetworkError as e:
        print(f"Ошибка сети телеграма: {e}")
    

# Сообщение тренера для создания индивидуальной программы тренировок 
async def send_message_trainer(message: Message):
    information = await rq_orm.AsyncOrm.information_about_user(tg_id=message.from_user.id) # Запрашиваем данные пользователя в человекочитаемом виде

    try:
        await bot.send_message(chat_id=TRAINER_ID, text=f"""
        🔔 <b>НОВЫЙ ЗАКАЗ НА ИНДИВИДУАЛЬНУЮ ПРОГРАММУ ТРЕНИРОВОК</b>
━━━━━━━━━━━━━━
👤 Клиент: @{message.from_user.username}
📋 Анкета клиента:
• 🎂 Возраст: {information['age']}
• 📏 Рост: {information['hight']}
• ⚖️ Вес: {information['weight']}
• 🚻 Пол: {information['gender']}
• 🔥 Уровень активности: {information['activity']}
• 😴 Сон (часов в сутки): {information['sleep_time']}
• 🚬 Привычки, требующие учёта: {information['bad_habbits']}
🎯 Цели и дополнительная информация:
{information['additional_information']}
        """, parse_mode="html")
        return True
    
    except TelegramNetworkError as e:
        print(f"Ошибка сети: {e}")