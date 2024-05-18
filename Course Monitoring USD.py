
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
bot = Bot(token="7009202598:AAEM6Sdq0QKP1eRWKVz46q7BWVzrNJk7wRA")

dp = Dispatcher()
@dp.message()
async def cmd_start(message:Message):
    await message.reply('My first bot started')

async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot is dissabled')
