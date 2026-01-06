from Database.models import ActivityPeople, GenderPeople


GENDER_REVERSE_MAP = {
    GenderPeople.man: "мужской",
    GenderPeople.woman: "Женский",
}


ACTIVITY_REVERSE_MAP = {
    ActivityPeople.very_hight: "Очень высокая",
    ActivityPeople.hight: "Высокая",
    ActivityPeople.middle: "Средняя",
    ActivityPeople.low: "Низкая",
}

SLEEP_TIME_REVERSE_MAP = {
    "very_long": "Более 10 часов",
    "long": "От 8 до 10 часов",
    "normal": "От 6 до 8 часов",
    "very_bad": "Менее 6 часов",
}


# Функция для маппинга данных из DB в челочекочитаемый вид
def user_data_to_human(user_data: dict) -> dict:
    return {
        "age": user_data.age,
        "hight": user_data.hight,
        "weight": user_data.weight,
        "gender": GENDER_REVERSE_MAP.get(user_data.gender, 'не указано'),
        "activity": ACTIVITY_REVERSE_MAP.get(user_data.activity, "не указано"),
        "sleep_time": SLEEP_TIME_REVERSE_MAP.get(user_data.sleep_time, "не указано"),
        "bad_habbits": (
            "есть вредные привычки" if user_data.bad_habbits else "отсутствуют"
        ),
        "additional_information": (
            "Нет" if user_data.additional_information is None else user_data.additional_information
        ),
    }