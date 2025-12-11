from sqlalchemy import select, insert

from Database.database import async_session
from Database.models import User_info, User_data


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