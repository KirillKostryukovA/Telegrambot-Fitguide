from datetime import *

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from Database.database import async_session
from Database.models import User_info, User_data, GenderPeople, ActivityPeople


now = datetime.now(timezone.utc) # Время сейчас

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
    async def update_user_paym_sub(tg_id: int):
        async with async_session() as session:
            user = await session.scalar(select(User_info).where(User_info.tg_id == tg_id))

            if not user:
                new_user = session.add(tg_id=tg_id)
                session.add(new_user)
                
                session.commit()
                return new_user

            # Сообщаем бд, что у пользователя теперь платная подписка
            user.paid_subcreption = True
            await session.commit()
            return True
        
    
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