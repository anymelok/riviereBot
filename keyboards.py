
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton



controlBtns = [
    [
        KeyboardButton(text='last'), 
        KeyboardButton(text='screen'),
        KeyboardButton(text='⏯')
    ],
    [
        KeyboardButton(text='mute'),
        KeyboardButton(text='🔉'),
        KeyboardButton(text='🔊')
    ]
]

controlKeyboard = ReplyKeyboardMarkup(keyboard=controlBtns, resize_keyboard=True)



mediaBtns = [
    [InlineKeyboardButton(text='Info', callback_data='call_showInfo'),
        InlineKeyboardButton(text = 'Screen', callback_data='call_sendScreen')]
        ]
inlkb = InlineKeyboardMarkup(inline_keyboard = mediaBtns)

