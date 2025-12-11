from sqlalchemy import insert, select, cast, func, Integer

from Database.database import Base, async_engine, async_session
from Database.models import User_data, User_info, GenderPeople, ActivityPeople


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
            # sqrt = select(
            #     User_info.id,
            #     cast(func.avg(User_info.tg_id), Integer).label("avg_tg_id")
            # ).select_from(User_info).filter(User_info.tg_id == tg_id)

            result = await session.execute(sqrt)
            id_pars = result.scalar_one_or_none()

            # Если пользователь не был найден 
            if id_pars is None:
                new_user = User_info(tg_id=tg_id)
                session.add(new_user)
                await session.flush()
                id_pars = new_user.id
                await session.commit()
                
            
            data = data.copy() # Подготавливаем данные

            # Гендер
            data['gender'] = GenderPeople.man if data['gender'] == "Мужской ♂️" else GenderPeople.woman

            # Активность
            if data['activity'] == "Каждый день":
                data['activity'] = ActivityPeople.very_hight
            elif data['activity'] == "3 раза в неделю":
                data['activity'] = ActivityPeople.middle               
            elif data['activity'] == "Более 3-х раз в неделю":
                data['activity'] = ActivityPeople.hight
            else:
                data['activity'] = ActivityPeople.low
            
            # Время сна
            if data['sleep_time'] == "Более 10 часов":
                data['sleep_time'] = "10+"
            if data['sleep_time'] == "8-10 часов":
                data['sleep_time'] = "8-10"
            if data['sleep_time'] == "6-8 часов":
                data['sleep_time'] = "6-8"
            if data['sleep_time'] == "Менее 6 часов":
                data['sleep_time'] = "6-"

            # Вредные привычки
            if data['bad_habbits'] == "Да, у меня есть вредная привычка/зависимость":
                data['bad_habbits'] = True
            else:
                data['bad_habbits'] = False

            # Доп. информация
            if data['additional_information'] == "У меня нет никаких ограничений/болезней/аллергий/т.д":
                data['additional_information'] = None

            # Добавляем информацию о пользователе в таблицу БД
            stmt = insert(User_data).values(
                id_us_info=id_pars,
                age=data['age'],
                gender=data['gender'],
                activity=data['activity'],
                sleep_time=data['sleep_time'],
                bad_habbits=data['bad_habbits'],
                additional_information=data['additional_information']
            )

            await session.execute(stmt)
            await session.commit()