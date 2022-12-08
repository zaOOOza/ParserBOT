import json
import os
import asyncio

from aiogram import Bot, types, Dispatcher
from aiogram.utils.markdown import hbold
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from parser import check_news

BOT_TOKEN = os.environ.get('BOT_TOKEN')


# '''to doo..., Добавить функцию, которая при нажатии на лайк, будет добавлять новость в избранное(новая таблица бд),
# с возможностью проссмотреть избранные новости'''
async def start(message: types.Message):
    start_button = ['Get news']
    keybord = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keybord.add(*start_button)
    await message.answer('News line', reply_markup=keybord)


# send to user all news
async def all_news(event: types.Message):
    while True:
        news_dict = check_news()
        if news_dict:
            print('Chek news...')
            news = str(f"""{hbold(news_dict['article_data_time'])}\n{news_dict['article_link']}""")
            await event.answer(news)
        else:
            await event.answer("Ждем свежих новостей")
        await asyncio.sleep(100)


# starting bot

async def main():
    bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
    try:
        disp = Dispatcher(bot=bot)
        disp.register_message_handler(start, commands={"start", "restart"})
        disp.register_message_handler(all_news, Text(equals='Get news'))
        await disp.start_polling()
    finally:
        await bot.close()


if __name__ == '__main__':
    asyncio.run(main())
