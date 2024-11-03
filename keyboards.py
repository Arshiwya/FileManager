from telethon.tl.types import ReplyKeyboardMarkup, KeyboardButtonRow, KeyboardButton
from models import Button

home_rows = [
    KeyboardButtonRow(buttons=[
        KeyboardButton(text=Button.ADD_FILE),
    ]),

    KeyboardButtonRow(buttons=[
        KeyboardButton(text=Button.SEARCH_FILE)
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
