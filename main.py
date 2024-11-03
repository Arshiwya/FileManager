from telethon import events
from telethon.events.newmessage import NewMessage
from telethon.events.common import EventBuilder
from telethon.types import User, Channel, PeerUser, UpdateNewMessage, Chat
from config import bot
from database import db

from functions import get_user, sign_user, change_step
from keyboards import home_markup, tos_markup
from reports import Report, ErrorReport, ReportCode
from messages import MessageText
from models import MyUser, Step, Button


@bot.on(event=NewMessage)
async def my_event_handler(event: NewMessage.Event):
    text = event.raw_text
    chat = event.chat

    if type(chat) == User:
        user = get_user(chat)

        if user is None:
            operation = sign_user(chat)

            if operation.status_code == ReportCode.SUCCESS:
                await bot.send_message(entity=chat.id, message=MessageText.SUCCESS_SIGN_IN)
            else:
                await bot.send_message(entity=chat.id, message=MessageText.SIMPLE_ERROR)

        else:
            user: MyUser

            if user.step == Step.TOS:

                if text == Button.ACCEPT_TOS:
                    change_step(user=user, step=Step.HOME)
                    await bot.send_message(entity=user.chat_id, message=MessageText.WELLCOME.format(name=user.name),
                                           buttons=home_markup)

                else:

                    await bot.send_message(entity=user.chat_id, message=MessageText.TERM_OF_SERVICE, buttons=tos_markup)

            elif user.step == Step.HOME:
                pass

        del user

    elif type(chat) == Channel:
        pass


bot.start()
bot.run_until_disconnected()
