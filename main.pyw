import cmds
from config_reader import config
import keyboards

import asyncio
import logging

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from datetime import datetime
from os import execv
import sys


logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.bot_token.get_secret_value())
aid = int(config.aid.get_secret_value())

ids = [
        aid,
        int(config.kid.get_secret_value()),
        int(config.sid.get_secret_value())
       ]


dp = Dispatcher()
dp['started_at'] = datetime.now()


@dp.message(Command('info'))
async def cmd_info(message: types.Message, started_at: str):
    if message.from_user.id == aid:

        start_time = started_at.strftime('%d.%m.%Y %H:%M:%S')
        wort_time = str(datetime.now() - started_at)[:-7]

        await message.answer(f'Bot started {start_time}\nWorking {wort_time}')
        await message.delete()


@dp.message(Command('r'))
async def restart(message):
    if message.from_user.id == aid:
        await message.delete()
        await execv(sys.executable, [sys.executable, *sys.argv])
        

@dp.message(Command('kys'))
async def restart(message):
    if message.from_user.id == aid:
        await message.delete()
        await message.answer('dying...')
        sys.exit()


@dp.message(F.text)
async def handle_text(message):
    if message.from_user.id == aid:
        await cmds.handle_text_commands(message)
        
        # Hidden users doesn't have user id
        # so i can't answer them manually
        
        # print(message.reply_to_message.forward_from.id)
    else:
        await message.forward(aid)


@dp.edited_message()
async def edited_message_handler(edited_message):
    if edited_message.from_user.id == aid:
        await cmds.handle_text_commands(edited_message)
    else:
        await edited_message.forward(aid)


@dp.message(F.video)
async def handle_video(message):
    if message.from_user.id in ids:
        await cmds.convertToNote(message, bot, message.from_user.id)
        await message.delete()
    else:
        await message.forward(aid)


@dp.message(F.audio)
async def handle_audio(message):
    if message.from_user.id in ids:
        await cmds.convertToVoice(message, bot, message.from_user.id)
        await message.delete()
    else:
        await message.forward(aid)


@dp.message()
async def handle_others(message):
    if message.from_user.id not in ids:
        await message.forward(aid)
    

async def main():
    await dp.start_polling(bot)
    cmds.loadCommands()
    await bot.send_message(aid, f'Bot started', reply_markup=keyboards.controlBtns)


if __name__ == "__main__":
    asyncio.run(main())