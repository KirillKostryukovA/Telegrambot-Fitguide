from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardRemove

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from app.user_panel import main_menu

import app.keyboards as kb

import Database.requests.orm as rq_orm
import Database.requests.core as rq_core


survey_router = Router()

# Машина состояния - опрос
class Survey_user(StatesGroup):
    age = State()
    gender = State()
    activity = State()
    sleep_time = State()
    bad_habbits = State()
    additional_information = State()


# Возраст
@survey_router.message(F.text == "📊 Пройти опрос")
async def survey_for_user1(message: Message, state: FSMContext):
    examination = await rq_orm.AsyncOrm.verification_data_survey(tg_id=message.from_user.id) # Проверяет, проходил ли ранее пользователь опрос

    # Если пользователь ранее проходил опросs
    if examination:
        await update_data_from_survey(message)
        return 
    
    await state.set_state(Survey_user.age) # В каком состоянии находится пользователь
    await message.answer("""
Отлично! Это самый важный шаг.

Сейчас мы пройдем короткий опрос (всего 5 вопросов). Моя задача — понять твои цели, уровень и условия, чтобы собрать идеальную программу именно для тебя.

Точные ответы = Максимальный результат.
""")
    await message.answer("Введите Ваш возраст:")

# Гендр
@survey_router.message(Survey_user.age)
async def survey_for_user2(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Введите возраст числом!")
        return
    
    await state.update_data(age=int(message.text)) # Сохраняем информацию о возрасте
    await state.set_state(Survey_user.gender)

    await message.answer("Отлично, теперь выберите свой пол:",reply_markup=kb.gender_kb)

# Активность
@survey_router.message(Survey_user.gender)
async def survey_for_user3(message: Message, state: FSMContext):
    await state.update_data(gender=message.text)
    await state.set_state(Survey_user.activity)

    await message.answer("Сколько раз в неделю Вы обычно занимаетесь физической активностью (спортом, тренировками, ходьбой)?", reply_markup=kb.activity_kb)


# Сон
@survey_router.message(Survey_user.activity)
async def survey_for_user4(message: Message, state: FSMContext):
    await state.update_data(activity=message.text)
    await state.set_state(Survey_user.sleep_time)

    await message.answer("Сколько часов в день Вы спите?", reply_markup=kb.sleep_time_kb)


# Плохие привычки
@survey_router.message(Survey_user.sleep_time)
async def survey_for_user5(message: Message, state: FSMContext):
    await state.update_data(sleep_time=message.text)
    await state.set_state(Survey_user.bad_habbits)

    await message.answer("Последний вопрос. Есть ли у Вас вредные привычки/зависимоти по типу курения/алкоголизма?", reply_markup=kb.bad_habbits_kb)


# Дополнительные медицинские данные
@survey_router.message(Survey_user.bad_habbits)
async def survey_for_user6(message: Message, state: FSMContext):
    await state.update_data(bad_habbits=message.text)
    await state.set_state(Survey_user.additional_information)

    await message.answer("""
Последний и очень важный вопрос для вашей безопасности. 

Пожалуйста, укажите любые медицинские противопоказания, хронические заболевания, травмы (в т.ч. старые), аллергии или иные состояния здоровья, которые нам необходимо учитывать при разработке вашей персональной программы тренировок.
                         
Если ничего подобного у Вас нет, нажмите на кнопку снизу
""", reply_markup=kb.additional_information)


# Сохраняем запрошенные данные в виде словаря для отправки в БД
@survey_router.message(Survey_user.additional_information)
async def survey_for_user7(message: Message, state: FSMContext):
    await state.update_data(additional_information=message.text)
    await message.answer("Спасибо большое за прохождение опроса, исходя из Ваших данных мы отправим Вам подходящую программу тренировок!", reply_markup=ReplyKeyboardRemove())

    data = await state.get_data() # Храним всю запрошенную информацию в виде словаря

    await rq_core.AsyncCore.insert_info_about_user(tg_id=message.from_user.id, data=data) # Возвращаем все данные в функцию в Core
    await state.clear() # Очищаем собранную информацию


# Если пользователь ранее проходил опрос, то бот будет спрашивать, не хочет ли он поменять данные
async def update_data_from_survey(message: Message):
    await message.answer("Вы уже проходили опрос ранее. Хотите пройти опрос заново? Это займёт всего 3-4 минуты. Ваш старый план будет автоматически скорректирован.",
                         reply_markup=kb.update_data_survey_kb)
    

# Если пользователь не хочет обновлять данные с опроса
@survey_router.message(F.text == "Нет, всё актуально")
async def dont_update_data_survey(message: Message, state: FSMContext):
    await state.clear()
    await main_menu(message)
    return 


# Если пользователь хочет обновить данные с опросаs
@survey_router.message(F.text == "Да, обновить данные")
async def update_data_from_survey_start(message: Message, state: FSMContext):
    await state.set_state(Survey_user.age)
    await message.answer("Введите Ваш возраст:")