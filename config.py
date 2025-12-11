import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from pydantic_settings import SettingsConfigDict, BaseSettings


# Данные базы данных
class Base_Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str 

    @property
    def async_db_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


# Данные бота
load_dotenv() # Ищет файл .env
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Токен бота с диспетчером
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# База данных
settings_db = Base_Settings()