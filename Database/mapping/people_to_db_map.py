from Database.models import ActivityPeople, GenderPeople


""" МАППИНГ С ЧЕЛОВЕКОЧИТАЕМЫХ ДАННЫХ НА БАЗУ ДАННЫХ """

activity_map = {
    "very_hight": "Каждый день",
    "hight": "Более 3-х раз в неделю",
    "middle": "3 раза в неделю",
    "low": "Вообще не занимаюсь",
}

sleep_time_map = {
    "very_long": "Более 10 часов",
    "long": "8-10 часов",
    "normal": "6-8 часов",
    "very_bad": "Менее 6 часов",
}