import os
from dotenv import load_dotenv

from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.filters import CommandStart

import app.keyboards.inline_keyboards.admin_panel_kb as inl_kb


admin_panel_router = Router()


load_dotenv()
admins = int(os.getenv("ADMIN_ID"))


# Главное меню в админ панеле
@admin_panel_router.message(CommandStart())
async def main_menu_admin(message: Message):
    if message.from_user.id == admins:
        await message.answer("""
    👨‍💼 АДМИН-ПАНЕЛЬ | FitGuide

    Выберите действие:
    """, reply_markup=inl_kb.main_menu_kb)
        

# Главное меню в админ панеле (Через CallbackQuery)
@admin_panel_router.callback_query(F.data == "back_main_menu_admin")
async def main_menu_admin_callback(callback: CallbackQuery):
    await callback.answer()
    
    if callback.from_user.id == admins:
        await callback.message.edit_text("""
    👨‍💼 АДМИН-ПАНЕЛЬ | FitGuide

    Выберите действие:
    """, reply_markup=inl_kb.main_menu_kb)