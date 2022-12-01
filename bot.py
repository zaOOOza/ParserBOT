import json
import os
import asyncio

from aiogram import Bot, types, Dispatcher
from aiogram.utils.markdown import hbold
from aiogram.dispatcher.filters import Text

from parser import check_reuters, check_forcklog, chek_ecb

BOT_TOKEN = os.environ.get('BOT_TOKEN')


async def start(message: types.Message):
    start_button = ['ECB', 'Forklog', 'Reuters']
    keybord = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keybord.add(*start_button)
    await message.answer('News line', reply_markup=keybord)


# send to user all news, testedet.py...
async def ecb_news(event: types.Message):
    while True:
        news_dict = chek_ecb()
        if news_dict:
            print(f'{news_dict} ecb')
            for k, v in reversed(news_dict.items()):
                news = f"{hbold(v['article_data_time'])}\n" \
                       f"{v['article_link']}"
                await event.answer(news)
        else:
            await event.answer("Ждем свежих новостей ecb")
        await asyncio.sleep(30)


async def forklog_news(event: types.Message):
    while True:
        news_dict = check_forcklog()
        if news_dict:
            print(f'{news_dict} fork')
            for k, v in reversed(news_dict.items()):
                news = f"{hbold(v['article_data_time'])}\n" \
                       f"{v['article_link']}"

                await event.answer(news)
        else:
            await event.answer("Ждем свежих новостей fork")
        await asyncio.sleep(30)


async def reuters_news(event: types.Message):
    while True:
        news_dict = check_reuters()
        if news_dict:
            print(f'{news_dict} reut')
            for k, v in reversed(news_dict.items()):
                news = f"{hbold(v['article_data_time'])}\n" \
                       f"{v['article_link']}"

                await event.answer(news)
        else:
            await event.answer("Ждем свежих новостей reut")
        await asyncio.sleep(30)


# starting bot
async def main():
    bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
    try:
        disp = Dispatcher(bot=bot)
        disp.register_message_handler(start, commands={"start", "restart"})
        disp.register_message_handler(ecb_news, Text(equals='ECB'))
        disp.register_message_handler(forklog_news, Text(equals='Forklog'))
        disp.register_message_handler(reuters_news, Text(equals='Reuters'))
        await disp.start_polling()
    finally:
        await bot.close()


if __name__ == '__main__':
    asyncio.run(main())
