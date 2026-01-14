from datetime import *

from sqlalchemy import insert, select, update

from Database.database import Base, async_engine, async_session
from Database.models import User_data, User_info, GenderPeople, ActivityPeople


now = datetime.now(timezone.utc) 
BLOCK_TIME = timedelta(minutes=1) # Представляет разницу между двумя моментами времени


class AsyncCore():
    # Создание БД
    @staticmethod
    async def create_db():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


    # Сохранение данных о пользователе из опроса в БД
    @staticmethod
    async def insert_info_about_user(tg_id: int, data: dict):
        async with async_session() as session:
            sqrt = select(User_info.id).where(User_info.tg_id == tg_id) # айди пользователя, котрый будет использоваться для связи между схемами в БД
            result = await session.execute(sqrt)
            id_pars = result.scalar_one_or_none()

            # Если пользователь не был найден 
            if id_pars is None:
                new_user = User_info(tg_id=tg_id)
                session.add(new_user)
                await session.flush()
                id_pars = new_user.id
                await session.flush() # Получаем User_data.id

            # Ищем данные в User_data, чтобы в дальнейшем понять, обновлять нам данные или добавлять
            stmt1 = (
                select(User_data)
                .where(User_data.id_us_info==id_pars)
            )
            stmt1_execute = await session.execute(stmt1)
            stmt_data = stmt1_execute.scalars().all()
            
            
            data = data.copy() # Подготавливаем данные

            if not stmt_data:  
                # Добавляем информацию о пользователе в таблицу БД, если нет данных в User_data
                stmt = insert(User_data).values(
                    id_us_info=id_pars,
                    age=data['age'],
                    hight=data['hight'],
                    weight=data['weight'],
                    gender=data['gender'],
                    activity=data['activity'],
                    sleep_time=data['sleep_time'],
                    bad_habbits=data['bad_habbits'],
                    additional_information=data['additional_information']
                )
            else:
                stmt = update(User_data).where(User_data.id_us_info==id_pars).values(
                    age=data['age'],
                    hight=data['hight'],
                    weight=data['weight'],
                    gender=data['gender'],
                    activity=data['activity'],
                    sleep_time=data['sleep_time'],
                    bad_habbits=data['bad_habbits'],
                    additional_information=data['additional_information']
                )

            # Время, в течение которого пользователь не может проходить опрос                
            stmt_timeblock_survey = update(User_info).where(User_info.id==id_pars).values(
                survey_available_at=now + BLOCK_TIME # Допустим, время 16:51, + ещё 1 минута = 16:52 ==> Пока время не достигнет 16:52, пользователь не сможет пройти опрос
            )

            await session.execute(stmt)
            await session.execute(stmt_timeblock_survey)
            await session.commit()

    
    # Обновляем возраст в профиле
    @staticmethod
    async def update_age_in_profile(tg_id: int, age_user: int):
        async with async_session() as session:
            try:
                # Переменная хранит айди из User_info
                user_info = (
                    select(User_info.id)
                    .where(User_info.tg_id==tg_id)
                )
                
                await session.execute((
                    update(User_data)
                    .where(User_data.id_us_info==user_info)
                    .values(age=age_user)
                ))
                await session.commit()

            except Exception as e:
                print(f"Ошибка в core в update_age_in_profile: {e}")


    # Обновляем рост пользователя
    @staticmethod
    async def update_hight_in_profile(tg_id: int, hight_user: int):
        async with async_session() as session:
            try:
                # Переменная хранит айди из User_info
                user_info = (
                    select(User_info.id)
                    .where(User_info.tg_id==tg_id)
                )
                
                await session.execute((
                    update(User_data)
                    .where(User_data.id_us_info==user_info)
                    .values(hight=hight_user)
                ))
                await session.commit()

            except Exception as e:
                print(f"Ошибка в core в update_hight_in_profile: {e}")


    # Обновляем вес пользователя
    @staticmethod
    async def update_weight_in_profile(tg_id: int, weight_user: int):
        async with async_session() as session:
            try:
                # Переменная хранит айди из User_info
                user_info = (
                    select(User_info.id)
                    .where(User_info.tg_id==tg_id)
                )
                
                await session.execute((
                    update(User_data)
                    .where(User_data.id_us_info==user_info)
                    .values(weight=weight_user)
                ))
                await session.commit()

            except Exception as e:
                print(f"Ошибка в core: {e}")


    # Обновляем активность пользователя
    @staticmethod
    async def update_activity_in_profile(tg_id: int, data: str):
        async with async_session() as session:
            try:   
                user_info = select(User_info.id).where(User_info.tg_id==tg_id)

                await session.execute((
                    update(User_data)
                    .where(User_data.id_us_info==user_info)
                    .values(activity=data)
                ))

                await session.commit()

            except Exception as e:
                print(f"Произошла ошибка в core в update_activity_in_profile: {e}")


    # Обновляем время сна пользователя 
    @staticmethod
    async def update_sleep_time_in_profile(tg_id: int, data: str):
        async with async_session() as session:
            try:
                user_info = select(User_info.id).where(User_info.tg_id == tg_id)

                await session.execute((
                    update(User_data)
                    .where(User_data.id_us_info==user_info)
                    .values(sleep_time=data)
                ))

                await session.commit()

            except Exception as e:
                print(f"Произошла ошибка в core в update_sleep_time_in_profile: {e}")


    # Обновляем дополнительную информацию о пользователе
    @staticmethod
    async def update_additional_information_in_profile(tg_id: int, data: str):
        async with async_session() as session:
            try:
                user_info = select(User_info.id).where(User_info.tg_id == tg_id)

                await session.execute((
                    update(User_data)
                    .where(User_data.id_us_info==user_info)
                    .values(additional_information=data)
                ))

                await session.commit()

            except Exception as e:
                print(f"Произошла ошибка в core в update_additional_information_in_profile: {e}")