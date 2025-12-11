import asyncio
import logging
import tracemalloc

from config import dp, bot
from app.user_panel import user_router
from app.survey import survey_router
from app.training_program import program_training_router

from Database.requests.core import AsyncCore


tracemalloc.start() # Включает трассировку, отслеживающую распреление памяти в программе

# Основная функция, в которой у нас запускаются все функции
async def main():
    dp.include_router(user_router)
    dp.include_router(survey_router)
    dp.include_router(program_training_router)
    
    # Запуск бота
    await AsyncCore.create_db()
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    # except:
    #     await bot.session.close()
        


# Запуск нашего проекта
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())