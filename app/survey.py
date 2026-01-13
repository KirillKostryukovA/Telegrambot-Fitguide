from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from app.panels.user_panel import main_menu

import app.keyboards.Reply_keyboards.keyboards as kb
import app.keyboards.inline_keyboards.survey_keyboard as inl_kb

import Database.requests.orm as rq_orm
import Database.requests.core as rq_core


survey_router = Router()

# Машина состояния - опрос
class Survey_user(StatesGroup):
    age = State()
    hight = State()
    weight = State()
    gender = State()
    activity = State()
    sleep_time = State()
    bad_habbits = State()
    additional_information = State()


# Возраст
@survey_router.callback_query(F.data == "survey")
async def survey_for_user1(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    examination = await rq_orm.AsyncOrm.verification_data_survey(tg_id=callback.from_user.id) # Проверяет, проходил ли ранее пользователь опрос

    # Если пользователь ранее проходил опросs
    if examination:
        await update_data_from_survey(callback)
        return 
    
    await state.set_state(Survey_user.age) # В каком состоянии находится пользователь
    
    await callback.message.answer("""
Отлично! Это самый важный шаг.

Сейчас мы пройдем короткий опрос (всего 5 вопросов). Моя задача — понять твои цели, уровень и условия, чтобы собрать идеальную программу именно для тебя.

Точные ответы = Максимальный результат.
                                  
Введите Ваш возраст:
""")


# Рост пользователя
@survey_router.message(Survey_user.age)
async def survey_for_user2(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Введите возраст числом!")
        return 
    
    await state.update_data(age=int(message.text))
    await state.set_state(Survey_user.hight)
    await message.answer("Введите Ваш рост (см) числом:")


# Вес пользователя
@survey_router.message(Survey_user.hight)
async def survey_for_user3(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Введите рост числом!")
        return 
    
    await state.update_data(hight=int(message.text))
    await state.set_state(Survey_user.weight)

    await message.answer("Введите Ваш вес (кг) числом:")


# Гендр
@survey_router.message(Survey_user.weight)
async def survey_for_user4(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Введите вес числом!")
        return

    await state.update_data(weight=int(message.text)) # Сохраняем информацию о возрасте
    await state.set_state(Survey_user.gender)

    await message.answer("Отлично, теперь выберите свой пол:",reply_markup=inl_kb.gender_kb)


# Активность
@survey_router.callback_query(Survey_user.gender, F.data.startswith("gender"))
async def survey_for_user5(callback: CallbackQuery, state: FSMContext):
    gender_user = callback.data.split(":")[1]
    
    await callback.answer()
    await state.update_data(gender=gender_user)
    await state.set_state(Survey_user.activity)

    await callback.message.edit_text("Сколько раз в неделю Вы обычно занимаетесь физической активностью (спортом, тренировками, ходьбой)?", 
                                  reply_markup=await inl_kb.activity_kb())


# Сон
@survey_router.callback_query(Survey_user.activity, F.data.startswith("activity:"))
async def survey_for_user6(callback: CallbackQuery, state: FSMContext):
    activity_user = callback.data.split(":")[1]
    
    await callback.answer()
    await state.update_data(activity=activity_user)
    await state.set_state(Survey_user.sleep_time)

    await callback.message.edit_text("Сколько часов в день Вы спите?", 
                                  reply_markup=await inl_kb.sleep_time_kb())


# Плохие привычки
@survey_router.callback_query(Survey_user.sleep_time, F.data.startswith("sleep_time:"))
async def survey_for_user7(callback: CallbackQuery, state: FSMContext):
    sleep_time_user = callback.data.split(":")[1]
    
    await callback.answer()
    await state.update_data(sleep_time=sleep_time_user)
    await state.set_state(Survey_user.bad_habbits)

    await callback.message.edit_text("Есть ли у Вас вредные привычки/зависимоти по типу курения/алкоголизма?", 
                                  reply_markup=inl_kb.bad_habbits_kb)


# Дополнительные медицинские данные
@survey_router.callback_query(Survey_user.bad_habbits, F.data.startswith("bad_habbits:"))
async def survey_for_user8(callback: CallbackQuery, state: FSMContext):
    bad_habbits_user = callback.data.split(":")[1]
    
    await callback.answer()

    if bad_habbits_user == "presence_bad_habbits":
        await state.update_data(bad_habbits=True)
    else:
        await state.update_data(bad_habbits=False)

    await state.set_state(Survey_user.additional_information)

    await callback.message.edit_text("""
Последний и очень важный вопрос. 

Опишите, пожалуйста, с какой целью Вы хотите приобрести программу тренировок/план питания?

КРОМЕ ТОГО!
Пожалуйста, укажите любые медицинские противопоказания, хронические заболевания, травмы (в т.ч. старые), аллергии или иные состояния здоровья, которые нам необходимо учитывать при разработке вашей персональной программы тренировок.
""", parse_mode="html")


# Сохраняем запрошенные данные в виде словаря для отправки в БД
@survey_router.message(Survey_user.additional_information)
async def survey_for_user9(message: Message, state: FSMContext):
    await state.update_data(additional_information=message.text)

    data = await state.get_data() # Храним всю запрошенную информацию в виде словаря

    try:
        await rq_core.AsyncCore.insert_info_about_user(tg_id=message.from_user.id, data=data) # Возвращаем все данные в функцию в Core
        await state.clear() # Очищаем собранную информацию
        await message.answer("Спасибо большое за прохождение опроса, исходя из Ваших данных мы отправим Вам подходящую программу тренировок!", reply_markup=ReplyKeyboardRemove())

    except Exception as e:
        print(f"Неизвестная ошибка: {e}")


# Если пользователь ранее проходил опрос, то бот будет спрашивать, не хочет ли он поменять данные
async def update_data_from_survey(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Вы уже проходили опрос ранее. Хотите пройти опрос заново? Это займёт всего 3-4 минуты. Ваш старый план будет автоматически скорректирован.",
                         reply_markup=inl_kb.update_data_survey_kb)


# Если пользователь хочет обновить данные с опроса
@survey_router.callback_query(F.data == "update_data_survey")
async def update_data_from_survey_start(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    # Удаляем сообщение для красоты 
    await callback.message.delete()
    
    verify_survey_time = await rq_orm.AsyncOrm.verification_timeblock_survey(tg_id=callback.from_user.id)

    if verify_survey_time == False:
        await state.clear()
        await callback.message.answer("Извините, но на данный момент Вам не доступен опрос. Попробуйте в это же время завтра!")
        await main_menu(callback)
        return 
    
    await state.set_state(Survey_user.age)
    await callback.message.answer("Введите Ваш возраст:")