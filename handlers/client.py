from aiogram import F, types, Router, Bot
from aiogram.filters.command import CommandStart
from keyboard.kb import start_kb, change_kb
from db.db import DB
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import datetime
from config import WEATHER_API
import requests

sched = AsyncIOScheduler()

class ST(StatesGroup):
    locs = State()
    time = State()

router = Router()
WorksDB = DB()


@router.message(CommandStart())
async def start_cmd(message: types.Message, state: FSMContext):
    to_check = WorksDB.user_check(message.from_user.id)
    if to_check:
        await message.answer('Ваш прогноз уже настроен. Хотите поменять?', reply_markup=change_kb())
    else:
        await message.answer('Для придоставления вашей погоды нам нужны ваша геопозиция.\
 Для работы бота нажмите кнопку ниже', reply_markup=start_kb())
        await state.set_state(ST.locs)
        
        
@router.message(F.text == '/desc')
async def description_command(message: types.Message):
    await message.answer('Этот бот будет ежедневно в одно и то-же время присылать вам погоду.\n\
для настройки и начала работы с ботом напишите команду /start')
    
    
@router.message(F.location, ST.locs)
async def get_loc(message: types.Message, state: FSMContext):
    lat = message.location.latitude
    lon = message.location.longitude
    await state.update_data(user_id=message.chat.id)
    await state.update_data(lat=lat)
    await state.update_data(lon=lon)
    

    await message.answer('Отправьте время отправки в формате 00:00', reply_markup=types.reply_keyboard_remove.ReplyKeyboardRemove(remove_keyboard=True))
    await state.set_state(ST.time)
    
    
@router.message(ST.time)
async def time_handler(message: types.Message, state: FSMContext, bot: Bot):
    try:
        time = list(map(int, message.text.split(':'),))
    except Exception:
        await message.answer('Вы ввели неверный формат времени!')
        return
    await state.update_data(hour=time[0])
    await state.update_data(minute=time[1])
    
    date = await state.get_data()
    sched.add_job(work, trigger='cron', hour=time[0], minute=time[1], args=[bot, date['lon'], date['lat'], date['user_id']])
    WorksDB.user_add(date=date)
    await message.answer(f'Прогноз для вас успешно добавлен. Теперь вы будуте получать его каждый день в {message.text}')
    await state.clear()
    
    
async def work(bot: Bot, lan, lot, chat_id):
    params = {'key':WEATHER_API, 'q':'56.884321,60.513568', 'alerts':'no', 'lang':'ru'}
    res = requests.get(f'http://api.weatherapi.com/v1/current.json', params=params).json()
    text = f"""
        <em>Погода</em>🌨:
    
{res['current']['condition']['text']}
    
<b>Температура</b>: {res['current']['temp_c']} ℃
<i>Ощущается как: {res['current']['feelslike_c']}</i> ℃
    """
    await bot.send_message(chat_id=chat_id, text=text, parse_mode='HTML')

    
@router.callback_query(F.data == 'change')
async def change_all(callback: types.CallbackQuery):
    WorksDB.delete_user(callback.from_user.id)
    await callback.message.answer('Мы удалили ваш прогноз. Для того чтобы сделать новый\
пропишите команду /start')
    await callback.answer()
    
