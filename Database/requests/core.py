from sqlalchemy import insert, select, update

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
            

            # -----     Начало маппинга -----
            
            
            data = data.copy() # Подготавливаем данные

            # Гендер
            data['gender'] = GenderPeople.man if data['gender'] == "Мужской ♂️" else GenderPeople.woman

            # Активность
            activity_map ={
                "Каждый день": ActivityPeople.very_hight,
                "Более 3-х раз в неделю": ActivityPeople.hight,
                "3 раза в неделю": ActivityPeople.middle,
                "Вообще не занимаюсь": ActivityPeople.low,
            }

            data['activity'] = activity_map.get(data['activity'], ActivityPeople.low)
            

            # Время сна
            sleep_time_map = {
                "Более 10 часов": "10+",
                "8-10 часов": "8-10",
                "6-8 часов": "6-8",
                "Менее 6 часов": "6-",
            }

            data['sleep_time'] = sleep_time_map.get(data['sleep_time'], None)


            # Вредные привычки
            bad_habbits_map = {
                "Да, у меня есть вредная привычка/зависимость": True,
                "Нет, у меня нет вредных привычек/зависимостей": False,
            }

            data['bad_habbits'] = bad_habbits_map.get(data['bad_habbits'], False)


            # Доп. информация
            additional_information_map = {
                "У меня нет никаких ограничений/болезней/аллергий/т.д": None,
            }

            data['additional_information'] = additional_information_map.get(data['additional_information'], data['additional_information'])


            if not stmt_data:  
                # Добавляем информацию о пользователе в таблицу БД, если нет данных в User_data
                stmt = insert(User_data).values(
                    id_us_info=id_pars,
                    age=data['age'],
                    gender=data['gender'],
                    activity=data['activity'],
                    sleep_time=data['sleep_time'],
                    bad_habbits=data['bad_habbits'],
                    additional_information=data['additional_information']
                )
            else:
                stmt = update(User_data).where(User_data.id_us_info==id_pars).values(
                    age=data['age'],
                    gender=data['gender'],
                    activity=data['activity'],
                    sleep_time=data['sleep_time'],
                    bad_habbits=data['bad_habbits'],
                    additional_information=data['additional_information']
                )

            await session.execute(stmt)
            await session.commit()