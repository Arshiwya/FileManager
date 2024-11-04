from telethon.tl.types import ReplyKeyboardMarkup, KeyboardButtonRow, KeyboardButton
from telethon import Button as button
from models import Button, CallBackQueryPrefix, CallBackQuery
from telethon.tl.types import KeyboardButtonUserProfile

home_rows = [
    KeyboardButtonRow(buttons=[
        KeyboardButton(text=Button.ADD_FILE),
    ]),

    KeyboardButtonRow(buttons=[
        KeyboardButton(text=Button.SEARCH_FILE)
    ]),

    KeyboardButtonRow(buttons=[
        KeyboardButton(text=Button.MY_FILE)
    ]),

    KeyboardButtonRow(buttons=[
        KeyboardButton(text=Button.MANAGE_FILE)
    ]),
]

home_markup = ReplyKeyboardMarkup(rows=home_rows, resize=True)

tos_rows = [
    KeyboardButtonRow(buttons=[
        KeyboardButton(text=Button.ACCEPT_TOS),
    ]),

    KeyboardButtonRow(buttons=[
        KeyboardButton(text=Button.REJECT_TOS)
    ]),
]

tos_markup = ReplyKeyboardMarkup(rows=tos_rows, resize=True)

back_markup = ReplyKeyboardMarkup(
    rows=[KeyboardButtonRow(buttons=[
        KeyboardButton(text=Button.BACK),
    ]), ], resize=True
)


def make_manage_inline_markup(file_id):
    markup = [
        [
            button.inline(text='Manage File ⚙️', data=f'manage-{file_id}'),

        ],

    ]

    return markup


def make_manage_panel_inline_markup(file_id):
    markup = [
        [
            button.inline(text='Set caption 🔖', data=f'{CallBackQueryPrefix.SET_FILE_TITLE}{file_id}'),
            button.inline(text='Delete file 🗑', data=f'{CallBackQueryPrefix.DELETE_FILE}{file_id}'),

        ],

        [

            button.inline(text='🔴 Close panel 🔴', data=f'{CallBackQuery.CLOSE_PANEL}'),

        ],

    ]

    return markup
