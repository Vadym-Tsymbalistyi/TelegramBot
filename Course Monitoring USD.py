import asyncio
import requests
import sqlite3
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from aiogram import Bot, Dispatcher, F, types
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart, Command

bot = Bot(token="7009202598:AAEM6Sdq0QKP1eRWKVz46q7BWVzrNJk7wRA")

dp = Dispatcher()

DB = 'exchange.db'


def parse_exchange():
    url = "https://www.google.com/finance/quote/USD-UAH"
    response = requests.get(url)
    bs = BeautifulSoup(response.text, "html.parser")
    exchange_rate_html = bs.find('div', class_="YMlKec fxKbKc")
    exchange_rate = exchange_rate_html.text.strip()
    print(exchange_rate)
    return exchange_rate




async def send_exchange_rate(chat_id):
    exchange_rate = parse_exchange()
    save_exchange_rate(exchange_rate)
    data = {'Timestamp': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")], 'Exchange Rate': [exchange_rate]}
    df = pd.DataFrame(data)
    filename = f'exchange_rate_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.xlsx'
    df.to_excel(filename, index=False)
    document = FSInputFile(filename)
    await bot.send_document(chat_id, document)


@dp.message(Command('get_exchange_rate'))
async def get_exchange_rate(message: types.Message):
    chat_id = message.chat.id
    await send_exchange_rate(chat_id)


def save_exchange_rate(exchange_rate):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS exchange_rate 
        (id  INTEGER PRIMARY KEY AUTOINCREMENT,
        time DATETIME DEFAULT current_time,
        exchange_rate FLOAT)  ''')
    cursor.execute('''INSERT INTO exchange_rate (exchange_rate) VALUES(?)''', (exchange_rate,))
    conn.commit()
    last_id = cursor.lastrowid
    conn.close()
    return last_id


# exchange_rate = 24.4
# last_id = save_exchange_rate(exchange_rate)
# print(f'Save id {last_id}')


# @dp.message(CommandStart())
# async def cmd_start(message: Message):
#    await message.answer('My first bot started')
#
#
# @dp.message(Command('help'))
# async def cmd_help(message: Message):
#    await message.answer('You have clicked on the help')
#
#
# @dp.message(F.text == 'I am good')
# async def good(message: Message):
#    await message.answer('SUPER')


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot is dissabled')
