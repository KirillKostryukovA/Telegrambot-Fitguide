from datetime import *

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from Database.database import async_session
from Database.models import User_info, User_data, GenderPeople, ActivityPeople
from Database.mapping.user_data_map import user_data_to_human


now = datetime.now(timezone.utc) # Время сейчас

# Список для того, чтобы зафиксировать дату подписки пользователя 
SUBSCRIPTION_TIME_MAP = {
    "sub_1_month" : timedelta(days=30),
    "sub_3_month" : timedelta(days=90),
    "sub_6_month" : timedelta(days=180),
    "sub_1_year" : timedelta(days=365),
}


class AsyncOrm():
    # Добавление tg_id пользователя в БД
    @staticmethod
    async def get_user_tg_id(tg_id: int):
        async with async_session() as session:
            sqrt = await session.scalar(select(User_info).where(User_info.tg_id == tg_id))

            if not sqrt:
                new_user = User_info(tg_id=tg_id)
                session.add(new_user)

                await session.commit()
                return new_user
            

    # Делаем нашему пользователю премиум подписку 
    @staticmethod
    async def update_user_paym_sub(tg_id: int, payload: str):
        async with async_session() as session:
            user = await session.scalar(select(User_info).where(User_info.tg_id == tg_id))

            if not user:
                new_user = User_info(tg_id=tg_id)
                session.add(new_user)
                
                await session.commit()
                return new_user
            
            # Время, в которое пользователь приобретёт подписку
            now = datetime.now(timezone.utc)
            duration = SUBSCRIPTION_TIME_MAP.get(payload) # Определяем срок подписки
            
            # Если пользователь не купил подписку
            if not duration:
                raise ValueError("Подписка не куплена, произошла ошибка")
            
            # Если подписка уже есть
            if user.subscription_duration and user.subscription_duration > now:
                user.subscription_duration += duration
            # Если нет подписки у пользователя
            else:
                user.subscription_duration = now + duration
            
            # Сообщаем бд, что у пользователя теперь платная подписка
            user.paid_subcreption = True
            await session.commit()
        
    
    # Проверяем, проходил ли пользователь ранее опрос
    @staticmethod
    async def verification_data_survey(tg_id: int):
        async with async_session() as session:
            sqrt = (
                select(User_data)
                .where(User_info.tg_id == tg_id)
                .options(selectinload(User_data.info))
            )

            result = await session.execute(sqrt)
            row = result.scalar_one_or_none()

            if row is None:
                return False
            
            return True
        
        
    # Проверяем, доступен ли опрос для пользователя
    @staticmethod
    async def verification_timeblock_survey(tg_id: int):
        async with async_session() as session:
            sqrt = await session.execute(select(User_info.survey_available_at).where(User_info.tg_id==tg_id))
            result = sqrt.scalar_one_or_none()

            # Если это время есть и если время в настоящий момент меньше того, что в таблице, то возвращаем False
            if result is not None and now < result:
                return False
            
            return True
        
    
    # Проверяем, есть ли у пользователя подписка
    @staticmethod
    async def verification_sub(tg_id: int):
        async with async_session() as session:
            user = await session.execute(select(User_info.paid_subcreption).where(User_info.tg_id == tg_id))
            result = user.scalar_one_or_none()

            # Если подписки нет, то значит нет :_)
            if result is False:
                return False
            
            return True
        

    # Информация о пользователе в человекочитаемом виде 
    @staticmethod
    async def information_about_user(tg_id: int) -> dict:
        async with async_session() as session:
            sqrt = await session.execute((
            select(User_data)
            .join(User_info)
            .where(User_info.tg_id==tg_id)
            .options(selectinload(User_data.info))
            ))
            user_dict = sqrt.scalar_one_or_none()

            return user_data_to_human(user_dict) # Маппинг из DB в человекочитаемый вид данныхs