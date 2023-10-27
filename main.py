from aiogram import Dispatcher, Bot
from aiogram.types import BotCommand, BotCommandScopeDefault
import asyncio
from config import TOKEN
from handlers.client import router, WorksDB, sched, work
import datetime
import requests

def scheduler_readd(bot):
    #Возобнавляем задания в apscheduler при запуске бота

    result = WorksDB.select_all()
    if result:
        for i in result:
            sched.add_job(work, trigger='cron', hour=i[3], minute=i[4], args=[bot, i[1], i[2], i[0]])
            

async def main():
    
    dp = Dispatcher()
    bot = Bot(TOKEN)
    dp.include_router(router)
    com = [BotCommand(command='/start', description='Начало работы ботом'),
           BotCommand(command='/desc', description='Узнать что умеет бот')]
    
    await bot.set_my_commands(commands=com, scope=BotCommandScopeDefault())
    scheduler_readd(bot)
    sched.start()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    
if __name__ == '__main__':
    asyncio.run(main())