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


def make_manage_inline_markup(rowid):
    markup = [
        [
            button.inline(text='Manage File ⚙️', data=f'manage-{rowid}'),

        ],

    ]

    return markup


def make_manage_panel_inline_markup(rowid, status):
    published_status = "Published ✅"
    draft_status = "Draft ⚠️"

    if status == 1:
        status_text = published_status
        prefix = CallBackQueryPrefix.DEACTIVATE_STATUS

    else:
        status_text = draft_status
        prefix = CallBackQueryPrefix.ACTIVE_STATUS

    markup = [
        [
            button.inline(text='Edit title 🔖', data=f'{CallBackQueryPrefix.EDITE_FILE_TITLE}{rowid}'),
            button.inline(text='Delete file 🗑', data=f'{CallBackQueryPrefix.DELETE_FILE}{rowid}'),

        ],
        [

            button.inline(text='File Status 🚦 :', data=f'{CallBackQuery.NULL}'),
            button.inline(text=f'{status_text}', data=f'{prefix}{rowid}'),

        ],
        [

            button.inline(text='Download link ⛓️', data=f'{CallBackQueryPrefix.DOWNLOAD_LINK}{rowid}'),
            button.inline(text=f'Empty yet', data=f'{CallBackQuery.NULL}'),

        ],

        [

            button.inline(text='🔴 Close panel 🔴', data=f'{CallBackQuery.CLOSE_PANEL}'),

        ],

    ]

    return markup


def make_delete_panel_inline_markup(rowid):
    markup = [
        [
            button.inline(text='Are you sure to delete this file ❓', data=f'{CallBackQuery.NULL}'),

        ],

        [
            button.inline(text='Yes ✅', data=f'{CallBackQueryPrefix.KILL_FILE}{rowid}'),
            button.inline(text='No ❌', data=f'{CallBackQueryPrefix.MANAGE}{rowid}'),

        ],

    ]

    return markup


def make_edit_title_panel_inline_markup(rowid):
    markup = [

        [
            button.inline(text='Set new title 🏷', data=f'{CallBackQueryPrefix.SET_FILE_TITLE}{rowid}'),
            button.inline(text='Delete title ✂️', data=f'{CallBackQueryPrefix.DELETE_FILE_TITLE}{rowid}'),

        ],

        [
            button.inline(text='Back to manage 🔙', data=f'{CallBackQuery.BACK_TO_MANAGE}'),

        ],

    ]

    return markup
