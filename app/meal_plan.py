import os
import asyncio

from dotenv import load_dotenv

from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.exceptions import TelegramNetworkError, TelegramAPIError

from app.payments import paid_subscription
from app.panels.user_panel import main_menu

import Database.requests.orm as rq_orm

from config import bot


meal_plan_router = Router()

load_dotenv()
TRAINER_ID = int(os.getenv("TRAINER_ID"))


# Индивидуальный план питания для пользователя, оплатившего подписку
@meal_plan_router.message(F.text == "Индивидуальный план питания")
async def personal_meal_plan(message: Message):
    is_paid = await rq_orm.AsyncOrm.verification_sub(tg_id=message.from_user.id)
    is_data_survey = await rq_orm.AsyncOrm.verification_data_survey(tg_id=message.from_user.id)

    # Если у пользователя нет подписки
    if is_paid is False:
        return await paid_subscription(message)
    # Если пользователь не проходил опрос
    elif is_data_survey is False:
        await message.answer("Для того, чтобы получить личный план питания Вам необходимо пройти опрос, на основании которого мы сделаем Вам подходящиый план питания!")
        return await main_menu(message)

    try:
        await message.answer("""
✅ Отлично! Ваши данные с опроса отправлены нашему тренеру.

    Он внимательно изучит ваши ответы и в ближайшие 24 часа подготовит вашу персональный план питания. Вы получите её прямо здесь, в этом чате.

    А пока предлагаем не терять время:

    🔥 Переходите в наш закрытый Telegram-канал — там уже кипит жизнь! Вы можете:
    • Познакомиться с участниками марафона
    • Узнать полезные фитнес-лайфхаки
    • Начать погружаться в атмосферу поддержки и мотивации

    Перейти в закрытый ТГ-канал

    Оставайтесь на связи! Если у вас срочный вопрос, вы всегда можете написать нам.
    """, request_timeout=30)

        await message_to_trainer_2(message)

    except TelegramNetworkError as e:
        print(f"Произошла ошибка сети: {e}")


# Сообщение тренеру от пользователя насчёт плана питания
async def message_to_trainer_2(message: Message):
    information = await rq_orm.AsyncOrm.information_about_user(tg_id=message.from_user.id)

    try:    
        await bot.send_message(chat_id=TRAINER_ID, text=f"""
        🔔 НОВЫЙ ЗАКАЗ: Индивидуальная программа тренировок
                               
        👤 Клиент: {message.from_user.first_name}
        📋 Исходные данные клиента:

            Возраст: {information['age']}

            Пол: {information['gender']}

            Уровень активности: {information['activity']}

            Режим сна (часов в сутки): {information['sleep_time']}

            Привычки, требующие учета: {information['bad_habbits']}

            Дополнительная информация и цели: {information['additional_information']}
        """, request_timeout=30)
        return True

    except TelegramNetworkError as e:
        print(f"Произошла ошибка сети: {e}")


async def message_to_trainer_2(message: Message):
    """Отправка данных тренеру с retry-логикой"""
    max_retries = 3
    retry_delay = 2
    
    try:
        information = await rq_orm.AsyncOrm.information_about_user(tg_id=message.from_user.id)
        
        if not information:
            print("❌ Данные пользователя не найдены")
            return
        
        # Формируем сообщение
        trainer_message = f"""🔔 НОВЫЙ ЗАКАЗ: Индивидуальный план питания

👤 Клиент: {message.from_user.first_name}
📱 Telegram ID: {message.from_user.id}
👤 Username: @{message.from_user.username or 'не указан'}

📋 Исходные данные клиента:

• Возраст: {information['age']}
• Пол: {information['gender'].value if hasattr(information['gender'], 'value') else information['gender']}
• Уровень активности: {information['activity'].value if hasattr(information['activity'], 'value') else information['activity']}
• Режим сна: {information['sleep_time']} ч/сутки
• Вредные привычки: {'Да' if information['bad_habbits'] else 'Нет'}

💬 Дополнительная информация и цели:
{information['additional_information'] or 'Не указано'}
"""
        
        # Попытки отправки с повторами
        for attempt in range(max_retries):
            try:
                await bot.send_message(
                    chat_id=TRAINER_ID,
                    text=trainer_message,
                    request_timeout=30
                )
                print(f"✅ Сообщение тренеру отправлено (попытка {attempt + 1})")
                return True
                
            except (TelegramNetworkError, TelegramAPIError) as e:
                if attempt < max_retries - 1:
                    print(f"⚠️ Попытка {attempt + 1} не удалась: {e}")
                    print(f"⏳ Повтор через {retry_delay} секунд...")
                    await asyncio.sleep(retry_delay)
                    retry_delay *= 2
                else:
                    print(f"❌ Все попытки отправки тренеру исчерпаны: {e}")
                    
    except Exception as e:
        print(f"❌ Критическая ошибка при отправке тренеру: {type(e).name}: {e}")
        return False