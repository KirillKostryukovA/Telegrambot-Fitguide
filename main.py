import asyncio
import logging
import tracemalloc

from config import dp, bot
from Database.requests.core import AsyncCore

from app.panels.user_panel import user_router
from app.survey import survey_router
from app.training_program import program_training_router
from app.payments import payment_router, warning_watcher
from app.technical_support import support_router
from app.meal_plan import meal_plan_router
from app.progress_user import user_progress_router


tracemalloc.start() # Включает трассировку, отслеживающую распреление памяти в программе

# Бот раз в 24 часа будет чекать подписку пользователя, при этом уведомлять его об истечении подписки        
async def on_startup(bot):
    asyncio.create_task(warning_watcher(bot))

# Основная функция, в которой у нас запускаются все функции
async def main():
    dp.include_router(user_router)
    dp.include_router(survey_router)
    dp.include_router(program_training_router)
    dp.include_router(meal_plan_router)
    dp.include_router(payment_router)
    dp.include_router(support_router)
    dp.include_router(user_progress_router)

    # Задачи, выполняемые ботом параллельно его действиям с пользователем
    dp.startup.register(on_startup) # Проверяет время окончания подписки

    # Запуск бота
    await AsyncCore.create_db()
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    # except:
    #     await bot.session.close()

# Запуск нашего проекта
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())