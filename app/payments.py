import os
import asyncio

from datetime import *
from dotenv import load_dotenv

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery

import app.keyboards.inline_keyboards.payment_keyboard as inl_kb

import Database.requests.orm as rq_orm
import Database.requests.core as rq_core

from config import bot


payment_router = Router()

# Токен для оплаты подписки
load_dotenv()
PROVIDER_TOKEN = os.getenv("PROVIDER_TOKEN")
CLOSE_TGK = os.getenv("CLOSE_TGK")


"""     ----- Платная подписка для пользователя -----     """

# Просмотр подписки
@payment_router.callback_query(F.data == "my_subscribe")
async def my_subscription(callback: CallbackQuery):
    callback.answer()
    
    is_paid = await rq_orm.AsyncOrm.verification_sub(tg_id=callback.from_user.id)

    if is_paid == False:
        await callback.message.edit_text("""
🔓 Полный доступ закрыт

У вас пока не активирована подписка, которая открывает ключевые возможности для вашего прогресса. Но это легко исправить!

✨ С подпиской вы получите:
• Индивидуальную программу тренировок от тренера
• Персональный план питания, созданный под ваши цели
• Участие в марафоне с поддержкой и призами
• Прямую связь с экспертом для корректировок

🚀 Начните меняться уже сегодня — откройте доступ ко всему функционалу!
""", reply_markup=inl_kb.paid_subscription_kb)
    else:
        data_dict = await rq_orm.AsyncOrm.information_about_user_info_one(tg_id=callback.from_user.id)
        subscription_time = data_dict.subscription_duration.strftime('%Y-%m-%d')

        await callback.message.edit_text(f"""
✅ Ваша подписка активна!

Спасибо, что с нами. Доступ ко всем премиум-функциям открыт до {subscription_time} (Год-месяц-день).

✨ Вам доступно:
• Персональная программа тренировок
• Индивидуальный план питания
• Участие в марафонном комьюнити
• Поддержка тренера

🔄 Хотите продолжить путь без перерывов?
Вы можете продлить подписку сейчас на выгодных условиях — так ваша программа и прогресс не прервутся ни на день.
""", reply_markup=inl_kb.paid_subscription_kb)


# Покупка подписки
@payment_router.callback_query(F.data == "buy_subscribe")
async def paid_subscription(callback: CallbackQuery):
    await callback.answer()
    
    await callback.message.edit_text("""
🎯 Для получения персонализированной программы тренировок и полного доступа к функционалу необходима подписка

Что входит в подписку:

    Персональная программа тренировок — разработана профессиональным тренером. Вы сможете задавать вопросы и получать корректировки напрямую.

    Участие в закрытом марафоне — доступ в приватный чат, где вы вместе с единомышленниками будете совершенствовать своё тело. Лучшие результаты — щедрые подарки от нас.

    Эксклюзивные материалы — гайды, чек-листы и «плюшки», которые помогут сделать путь к цели проще и эффективнее.

💎 Это не просто программа — это ваша персональная система преобразования.

Готовы начать? Оформите подписку, и мы отправим вам детали доступа в течение 5 минут.
""", reply_markup=inl_kb.paid_subscription_kb)
    

# Приобритение платной подписки
@payment_router.callback_query(F.data == "buy_subscribe_now")
async def purchasing_ps(callback: CallbackQuery):
    await callback.answer()
    
    await callback.message.edit_text("""
💰 Стоимость подписки (оплата через WebApp):
• 1 месяц — 399 ₽
• 3 месяца — 699 ₽ (эффективно 233 ₽/мес)
• 6 месяцев — 999 ₽ (эффективно 166 ₽/мес)
• 1 год — 1 700 ₽ (эффективно 142 ₽/мес)

Готовы начать?
Оплатите подписку в WebApp, и мы отправим вам детали доступа в течение 5 минут.
""", reply_markup=inl_kb.purchasing_ps_kb)
    

# Подписка на 3 дня 
@payment_router.callback_query(F.data == "sub_3_days")
async def three_days_payment_sub(callback: CallbackQuery):
    await callback.message.answer_invoice(
        title="Подписка на 3 дня",
        description="Доступ ко всем функциям в течение 3-х дней",
        payload="sub_3_days",
        provider_token=PROVIDER_TOKEN,
        currency="RUB",
        prices=[LabeledPrice(label="3 дня", amount=30000),],
        start_parameter="sub_3d"
    )

    await callback.answer()


# Подписка на 1 месяц
@payment_router.callback_query(F.data == "sub_1_month")
async def one_month_payment_sub(callback: CallbackQuery):
    await callback.message.answer_invoice(
        title="Подписка на 1 месяц",
        description="Доступ ко всем функциям на 1 месяц",
        payload="sub_1_month",
        provider_token=PROVIDER_TOKEN,
        currency="RUB",
        prices=[LabeledPrice(label="1 месяц", amount=39900),], # amount всегда в копейках!!!!!
        start_parameter="sub_1"
    )

    await callback.answer() # ЭТО ОБЯЗАТЕЛЬНО ВСЕГДА!!!!! БЕЗ НЕГО CALLBACK_QUERY не будет работать


# Подписка на 3 месяца
@payment_router.callback_query(F.data == "sub_3_month")
async def three_month_payment_sub(callback: CallbackQuery):
    await callback.message.answer_invoice(
        title="Подписка на 3 месяца",
        description="Доступ ко всем функциям на 3 месяца",
        payload="sub_3_month",
        provider_token=PROVIDER_TOKEN,
        currency="RUB",
        prices=[LabeledPrice(label="3 месяца", amount=69900),],
        start_parameter="sub_3"
    )

    await callback.answer()


# Подписка на 6 месяцев
@payment_router.callback_query(F.data == "sub_6_month")
async def six_month_payment_sub(callback: CallbackQuery):
    await callback.message.answer_invoice(
        title="Подписка на 6 месяцев",
        description="Доступ ко всем функциям на 6 месяцев",
        payload="sub_6_month",
        currency="RUB",
        provider_token=PROVIDER_TOKEN,
        prices=[LabeledPrice(label="6 месяцев", amount=99900),],
        start_parameter="sub_6"
    )

    await callback.answer()


# Подписка на год
@payment_router.callback_query(F.data == "sub_1_year")
async def one_year_payment_sub(callback: CallbackQuery):
    await callback.message.answer_invoice(
        title="Подписка на 1 год",
        description="Доступ ко всем функциям на 1 год",
        payload="sub_1_year",
        currency="RUB",
        provider_token=PROVIDER_TOKEN,
        prices=[LabeledPrice(label="1 год", amount=170000),],
        start_parameter="sub_1_year"
    )

    await callback.answer()


# Функция, которая даёт подтверждение телеграмму об оплате подписки. Обрабатывает заказ (подписку)
@payment_router.pre_checkout_query()
async def pre_checkout(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)


# Если пользоватлель успешно оплатит подписку
@payment_router.message(F.successful_payment)
async def successful_payment(message: Message):
    payload = message.successful_payment.invoice_payload
    
    await rq_orm.AsyncOrm.update_user_paym_sub(message.from_user.id, payload=payload)
    await message.answer("""
🎉 Оплата прошла успешно! Добро пожаловать в клуб!

Твой доступ к премиум-контенту активирован. С этого момента твоё преображение — наш общий приоритет.

🔥 Теперь тебе доступно:

✅ Индивидуальная программа тренировок — твой личный план силы, созданный и курируемый профессиональным тренером.
✅ Индивидуальный план питания — персональный рацион, который будет работать именно на твои цели.
✅ Закрытый ТГ-канал с марафоном — твоё комьюнити для мотивации, поддержки и гонки за крутыми призами.
""")
    
    # Сразу же даём пользователю ссылку на закрытый ТГК
    invite = await bot.create_chat_invite_link(
        chat_id=CLOSE_TGK,
        member_limit=1, # Только для входа на 1 раз
    )

    await message.answer(f"""
🔒 Ваша персональная ссылка:\n{invite.invite_link}\n
⚠️ Ссылка одноразовая и действует 5 минут"
""")
    
    
# Если оплата не прошла    
@payment_router.message(F.failed_payment)
async def failed_payments(message: Message):
    await message.answer("❌ Оплата не прошла. Пожалуйста, попробуйте еще раз.")


# Если до окончания подписки остаётся 3 дня, то мы должны обязательно напомнить об этом пользователя
async def warning_watcher(bot):
    while True:
        users = await rq_orm.AsyncOrm.information_about_user_info()

        now = datetime.now(timezone.utc) # Время на данный момент

        for user in users:
            if user.subscription_duration is None:
                continue
            if user.subscription_warned == True:
                continue
            else:
                reminds = user.subscription_duration - now 
                tg_id_user = user.tg_id

                # Если разница меньше 3 дней, то отправляем уведомление
                if timedelta(days=2) < reminds <= timedelta(days=3):
                    await bot.send_message(
                        chat_id=tg_id_user,
                        text="""
🔄 Ваша подписка активна ещё 3 дня!\n
Чтобы не потерять доступ к персональной программе, плану питания и марафону — вовремя продлите подписку.
""", reply_markup=inl_kb.paid_subscription_kb)
                if reminds <= timedelta(days=0):
                    await bot.send_message(
                        chat_id=tg_id_user,
                        text="""
⚠️ Доступ приостановлен\n
Ваша подписка истекла. Чтобы возобновить работу с персональной программой, планом питания и продолжить участие в марафоне — необходимо обновить подписку.
\n
🔓 Что вы сейчас не можете использовать:
• Вашу индивидуальную программу тренировок и питания
• Закрытый марафон и чат поддержки
• Обновления и персональные рекомендации
""", reply_markup=inl_kb.paid_subscription_kb)
                    await rq_core.AsyncCore.warning_is_true(tg_id=tg_id_user) # Для того, чтобы пользователь больше не получал уведомление от бота об истекающей подписке
                    await rq_core.AsyncCore.delete_subs_user(tg_id=tg_id_user)
                    
        # Бот будет присылать уведомление в периоде 24 часа
        await asyncio.sleep(24 * 60 * 60)