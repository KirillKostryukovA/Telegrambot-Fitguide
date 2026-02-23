import os
from dotenv import load_dotenv

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.filters.command import CommandStart

import Database.requests.orm as rq_orm

# import app.keyboards.keyboards as kb
import app.keyboards.inline_keyboards.main_menu_keyboard as inl_kb

from app.panels.admin_panel.admin_menu import main_menu_admin


user_router = Router()

load_dotenv()
admins = int(os.getenv("ADMIN_ID"))


# Главное меню (вызов через Start)
@user_router.message(CommandStart())
async def main_menu(message: Message):
    # Если пользователь есть в админах
    if message.from_user.id == admins:
        return await main_menu_admin(message)
    
    photo_url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTFx0gyiLDo9h9d22mf0rThfr9RuJ5ciGrj3Q&s'
    wellcome_text = f"""
🏋️‍♂️ Привет, {message.from_user.first_name}!

Я — твой личный тренер и наставник по питанию прямо здесь, в Telegram! Моя цель — помочь тебе кардинально преобразить свою форму, силу и выносливость.

Выбери, с чего начнем свой путь:

• 📊 Пройти опрос — чтобы я создал персональную программу под твои цели.
• 🎯 Индивидуальная программа тренировок — готовая программа, рассчитанная именно на тебя (цели, уровень, инвентарь).
• 🥗 План питания конкретно под тебя — персонализированный рацион с учетом твоих параметров и предпочтений.
• 💪 Готовые тренировки — планы на силу, массу, рельеф или выносливость.
• 📈 Мой прогресс — отслеживать результаты и достижения.
• ❓ Помощь / FAQ — как пользоваться ботом.

🎯 Главное — начать. Первый шаг уже сделан!
"""
    
    await rq_orm.AsyncOrm.get_user_tg_id(message.from_user.id) # Функция, чтобы получить tg_id пользователя

    # Присылаем фото с подписью
    await message.answer_photo(
        photo=photo_url
    )
    await message.answer(
        text=wellcome_text,
        reply_markup=await inl_kb.main_menu_kb()
    )


# Главное меню (вызов через Start)
@user_router.callback_query(F.data == "back_main_menu")
async def main_menu(callback: CallbackQuery):
    await callback.answer()

    wellcome_text = f"""
🏋️‍♂️ Привет, {callback.from_user.first_name}!

Я — твой личный тренер и наставник по питанию прямо здесь, в Telegram! Моя цель — помочь тебе кардинально преобразить свою форму, силу и выносливость.

Выбери, с чего начнем свой путь:

• 📊 Пройти опрос — чтобы я создал персональную программу под твои цели.
• 🎯 Индивидуальная программа тренировок — готовая программа, рассчитанная именно на тебя (цели, уровень, инвентарь).
• 🥗 План питания конкретно под тебя — персонализированный рацион с учетом твоих параметров и предпочтений.
• 💪 Готовые тренировки — планы на силу, массу, рельеф или выносливость.
• 📈 Мой прогресс — отслеживать результаты и достижения.
• ❓ Помощь / FAQ — как пользоваться ботом.

🎯 Главное — начать. Первый шаг уже сделан!
"""
    
    await rq_orm.AsyncOrm.get_user_tg_id(callback.from_user.id) # Функция, чтобы получить tg_id пользователя
    
    await callback.message.edit_text(
            text=wellcome_text,
            reply_markup=await inl_kb.main_menu_kb()
        )