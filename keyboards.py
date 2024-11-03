from telethon.tl.types import ReplyKeyboardMarkup, KeyboardButtonRow, KeyboardButton

home_rows = [
    KeyboardButtonRow(buttons=[
        KeyboardButton(text='افزودن فایل'),
    ]),

    KeyboardButtonRow(buttons=[
        KeyboardButton(text='جستوجو فایل')
    ]),
]

home_markup = ReplyKeyboardMarkup(rows=home_rows, resize=True)

accept_tos_btn = 'I read and accept ✅'

tos_rows = [
    KeyboardButtonRow(buttons=[
        KeyboardButton(text='I read and accept ✅'),
    ]),

    KeyboardButtonRow(buttons=[
        KeyboardButton(text="I don't accept ❌")
    ]),
]

tos_markup = ReplyKeyboardMarkup(rows=tos_rows, resize=True)
