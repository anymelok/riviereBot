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


aid = 356484895


logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.bot_token.get_secret_value())

# print(not (config.cock_sucken))

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


@dp.message(F.text)
async def handle_text(message):
    if message.from_user.id == aid:
        await cmds.handle_text_commands(message)
        # await message.delete()
    else:
        await message.forward(aid)


@dp.message(F.video)
async def handle_video(message):
    if message.from_user.id == aid:
        await cmds.convertToNote(message, bot, aid)
        await message.delete()
    else:
        await message.forward(aid)


@dp.message(F.audio)
async def handle_audio(message):
    if message.from_user.id == aid:
        await cmds.convertToVoice(message, bot, aid)
        await message.delete()
    else:
        await message.forward(aid)

@dp.message()
async def handle_others(message):
    if message.from_user.id != aid:
        await message.forward(aid)


# @dp.callback_query(F.data.startswith('call_'))
# async def sendScreen(call: types.CallbackQuery, started_at: str):
#     if call.data == 'call_sendScreen':
#         await bot.send_photo(aid, cmds.getScreen(), 
#                              reply_markup=kb)
    
#     if call.data == 'call_showInfo':
#         start_time = started_at.strftime('%d.%m.%Y %H:%M:%S')
#         wort_time = str(datetime.now() - started_at)[:-7]

#         await bot.send_message(aid, f'Bot started {start_time}\nWorking {wort_time}',
#                                reply_markup=kb)

#     await cmds.handle_text_commands(cmds.replyMes)
    

async def main():
    await dp.start_polling(bot)
    cmds.loadCommands()
    await bot.send_message(aid, f'Bot started', reply_markup=keyboards.controlBtns)


if __name__ == "__main__":
    asyncio.run(main())