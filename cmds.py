from aiogram.types import FSInputFile

from subprocess import Popen, STARTUPINFO, STARTF_USESHOWWINDOW
import sys
from os import popen
from mss import mss
from validators import url
from webbrowser import open as openInBrowser
from keyboard import send, write

import keyboards
import readWrite

startupinfo = STARTUPINFO()
startupinfo.dwFlags |= STARTF_USESHOWWINDOW

cmds = {}
lastCommand = ''


# Функция хендлинга текста как команд
async def handle_text_commands(message):
    global lastCommand

    # Если ссылка, открывает браузер с этой ссылкой
    if url(message.text):
        openInBrowser(message.text, new=0, autoraise=True)
    
    commands = message.text.split('//')

    for textCommand in commands:

        command = textCommand.lower().split()[0]
        print(command)

        match command:
            
            # Выдать кнопки меню вместо клавиатуры
            case 'menu': 
                await message.answer('Menu', reply_markup=keyboards.controlKeyboard)

            # Нажать кнопку на клавиатуре компа
            case 'send' | 's':
                key = await sendKey(textCommand)
                await message.answer(key)
            
            # Написать что-то на компе
            case 'w' | 'т':
                text = await writeLine(textCommand)
                await message.answer(f'Wrote {text}')

            # Выключить/включить блютуз
            case 'btoff':
                btToggle('Off')

            case 'bton':
                btToggle('Off')

            # Отправить скриншот
            case 'screen':
                await deleteMessage(message)
                await message.answer_photo(getScreen())

            case 'play/pause' | '⏯':
                await deleteMessage(message)
                send('play/pause media')
            
            case 'volup' | '🔊':
                await deleteMessage(message)
                send('volume up')
                send('volume up')
            
            case 'voldown' | '🔉':
                await deleteMessage(message)
                send('volume down')
                send('volume down')

            case 'mute' | '🔈':
                await deleteMessage(message)
                send('volume mute')

            # Изменить масштаб интерфейса
            # Удобно когда с телефона надо подключиться к компу
            case 'scale':
                scale = await setScale(message)
                await deleteMessage(message)
                await message.answer(f'Scale set to {scale}')
            
            # Выполнение команды в cmd
            case 'cmd':
                output = popen(f'cmd /c chcp 65001 & {message.text[4:]}').read()
                if not output == 'Active code page: 65001':
                    message.answer(f'cmd: {output[:-1].replace("Active code page: 65001","")}') 

            # Выполнение последней команды
            case 'last':
                await deleteMessage(message)
                await handle_text_commands(message = lastCommand)

            case _:
                print(command)

                # Смотрим команды в commands.json и выполняем
                cmds = loadCommands()

                if command in cmds.keys():
                    message.answer(f'Command found: {command} - {cmds[command]}')
                    sendCommand(command)
                else:
                    message.answer('Unknown command')

    if command != 'last':
        lastCommand = message


def getScreen():
    mss().shot()
    screenshot = FSInputFile('monitor-1.png')
    return screenshot


def btToggle(turn):
    if (turn):
        status = 'On'
    else:
        status = 'Off'

    Popen(f'powershell.exe -WindowStyle hidden -ExecutionPolicy bypass \
          -file "files/bluetooth.ps1" -BluetoothStatus {status}', stdout=sys.stdout).wait()
    
    return status


async def sendKey(textCommand):
    key = str(textCommand.split(' ')[1])
    send(key)
    return key


async def writeLine(textCommand):
    line = (textCommand[2:])
    write(line)
    return line


async def setScale(textCommand):
    scale = textCommand.split()[1]
    Popen(f'files/setDpi.exe {scale}')
    return scale


async def convertToNote(message, bot, aid):
    file_id = message.video.file_id
    file = await bot.get_file(file_id)
    await bot.download_file(file.file_path, 'files/videonote.mp4')
    
    cropToSquare('files/videonote.mp4')

    await bot.send_video_note(aid, FSInputFile('files/videonoter.mp4'))
        

async def convertToVoice(message, bot, aid):
    file_id = message.audio.file_id
    file = await bot.get_file(file_id)
    await bot.download_file(file.file_path, 'files/audio.mp3')

    Popen('ffmpeg -i "files/audio.mp3" -vn -b:a 0.03M -loglevel quiet\
           -acodec libopus -y "files/voice.ogg"',
           startupinfo=startupinfo).wait()

    await bot.send_voice(aid, FSInputFile('files/voice.ogg'))


async def deleteMessage(message):
    try:
        await message.delete()
    except:
        pass


def cropToSquare(video):
    Popen(f'ffmpeg -i "{video}" -loglevel quiet\
        -vf "crop=min(iw\,ih):min(iw\,ih), scale=512x512" -y "files/videonoter.mp4"',
        startupinfo=startupinfo).wait()
    

def sendCommand(cmd):
    print('sendCommand')
    cmds = loadCommands()
    print(cmds[cmd])
    Popen(cmds[cmd]).wait()


def loadCommands():
    global cmds
    cmds = readWrite.readJSON('commands.json')
    return cmds
