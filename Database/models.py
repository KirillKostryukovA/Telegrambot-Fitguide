import datetime 
from enum import Enum

from sqlalchemy import Integer, Enum as SqlEnum, text, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from Database.database import Base


# Гендер пользователя
class GenderPeople(Enum):
    man = "man"
    woman =  "woman"

# Активность пользователя
class ActivityPeople(Enum):
    low = "low"
    middle = "middle"
    hight = "hight"
    very_hight = "very_hight"


"""     ----- Модели базы данных -----     """

# Информация об аккаунте пользователя
class User_info(Base):
    __tablename__ = "user_infos"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(nullable=False)
    paid_subcreption: Mapped[bool] = mapped_column(default=False)
    subscription_duration: Mapped[int] = mapped_column(Integer, nullable=True)

    data: Mapped[list["User_data"]] = relationship(back_populates="info", cascade="all, delete-orphan")

    def __repr__(self):
        return f"User_info id={self.id}, tg_id={self.tg_id}, paid_subscreption={self.paid_subcreption}"


# Информация о спортивных характеристиках пользователя
class User_data(Base):
    __tablename__ = "user_datas"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_us_info: Mapped[int] = mapped_column(ForeignKey("user_infos.id"))
    age: Mapped[int] = mapped_column(Integer)
    gender: Mapped[GenderPeople] = mapped_column(SqlEnum(GenderPeople, name="genderpeople"))
    activity: Mapped[ActivityPeople] = mapped_column(SqlEnum(ActivityPeople, name="activitypeople"))
    sleep_time: Mapped[str] = mapped_column(String(15))
    bad_habbits: Mapped[bool] = mapped_column(default=False)
    additional_information: Mapped[str] = mapped_column(String(2500), nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(default=text("TIMEZONE('utc', now())"))
    updated_at: Mapped[datetime.datetime] = mapped_column(default=text("TIMEZONE('utc', now())"), onupdate=datetime.datetime.now())

    info: Mapped["User_info"] = relationship(back_populates='data')

    def __repr__(self):
        return f"<User_data id={self.id}, id_us_info={self.id_us_info}, age={self.age}, gender={self.gender}, activity={self.activity}, \
            sleep_time={self.sleep_time}, bad_habbits={self.bad_habbits}, additional_information={self.additional_information}, \
                created_at={self.created_at}, updated_at={self.updated_at}>"