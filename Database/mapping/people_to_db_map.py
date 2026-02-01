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


search_user_map = {
    "send_message_to_uniq_user": "💬 Написать сообщение",
    "change_data_user_by_admin": "✏️ Изменить данные",
    "back_main_menu_admin": "🏠 Вернуться в главное меню",
}


update_data_user_by_admin_map = {
    "change_gender": "Пол",
    "change_subscribe": "Подписка",
    "back_main_menu_admin": "🏠 Вернуться в главное меню",
}