import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from database import init_db
from handlers import start, pet

#токен
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

#инициализация
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
init_db()

#подключаем роутеры
dp.include_router(start.router)
dp.include_router(pet.router)

async def main():
    print("работает")
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())