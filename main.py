from telethon import events
from telethon.events.newmessage import NewMessage
from telethon.events.callbackquery import CallbackQuery
from telethon.types import User, Channel, MessageMediaPhoto, MessageMediaDocument
from config import bot

from functions import get_user, sign_user, change_step, add_file, get_user_files, get_file
from keyboards import home_markup, tos_markup, back_markup, make_manage_inline_markup
from reports import Report, ErrorReport, ReportCode
from messages import MessageText
from models import MyUser, Step, Button


@bot.on(event=NewMessage)
async def main_handler(event: NewMessage.Event):
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
            if text == '/start':
                change_step(user=user, step=Step.HOME)
                await bot.send_message(entity=user.chat_id, message=MessageText.WELLCOME.format(name=user.name),
                                       buttons=home_markup)

            elif user.step == Step.TOS:

                if text == Button.ACCEPT_TOS:
                    change_step(user=user, step=Step.HOME)
                    await bot.send_message(entity=user.chat_id, message=MessageText.WELLCOME.format(name=user.name),
                                           buttons=home_markup)

                else:

                    await bot.send_message(entity=user.chat_id, message=MessageText.TERM_OF_SERVICE, buttons=tos_markup)

            elif user.step == Step.HOME:

                if text == Button.ADD_FILE:
                    change_step(user=user, step=Step.SENDING_FILE)
                    await bot.send_message(entity=user.chat_id, message=MessageText.SEND_FILE, buttons=back_markup)

                elif text == Button.SEARCH_FILE:
                    pass

                elif text == Button.MY_FILE:
                    files = get_user_files(user)

                    if files is None:
                        await bot.send_message(entity=user.chat_id, message=MessageText.USER_NO_HAVE_FILE)

                    else:
                        await bot.send_message(entity=user.chat_id,
                                               message=MessageText.USER_FILES_COUNT.format(count=len(files)))

                elif text == Button.MANAGE_FILE:
                    change_step(user=user, step=Step.SENDING_FILE_ID_FOR_MANAGE)
                    await bot.send_message(entity=user.chat_id, message=MessageText.SEND_FILE_ID_FOR_MANAGE,
                                           buttons=back_markup)

            elif user.step == Step.SENDING_FILE:

                if text == Button.BACK:
                    change_step(user=user, step=Step.HOME)
                    await bot.send_message(entity=user.chat_id, message=MessageText.WELLCOME.format(name=user.name),
                                           buttons=home_markup)

                else:
                    if event.media:

                        if type(event.media) == MessageMediaPhoto:
                            change_step(user=user, step=Step.HOME)

                            chat_id = user.chat_id
                            message_id = event.message.id
                            file_id = add_file(chat_id=chat_id, message_id=message_id, file_type='image')
                            markup = make_manage_inline_markup(file_id=file_id)

                            await bot.send_message(entity=user.chat_id,
                                                   message=MessageText.IMAGE_FILE_SAVED.format(file_id=file_id),
                                                   buttons=markup)
                            await bot.send_message(entity=user.chat_id,
                                                   message=MessageText.WELLCOME.format(name=user.name),
                                                   buttons=home_markup)

                        elif type(event.media) == MessageMediaDocument:
                            change_step(user=user, step=Step.HOME)

                            chat_id = user.chat_id
                            message_id = event.message.id
                            file_id = add_file(chat_id=chat_id, message_id=message_id, file_type='doc')
                            markup = make_manage_inline_markup(file_id=file_id)

                            await bot.send_message(entity=user.chat_id,
                                                   message=MessageText.FILE_SAVED.format(file_id=file_id),
                                                   buttons=markup)

            elif user.step == Step.SENDING_FILE_ID_FOR_MANAGE:
                if text == Button.BACK:
                    change_step(user=user, step=Step.HOME)
                    await bot.send_message(entity=user.chat_id, message=MessageText.WELLCOME.format(name=user.name),
                                           buttons=home_markup)

                else:
                    try:
                        file_id = int(text)
                        file = get_file(file_id)

                        if file is None:
                            await bot.send_message(entity=user.chat_id, message=MessageText.FILE_NOT_FOUND,
                                                   buttons=back_markup)

                        else:
                            file_chat_id = file[1]
                            file_message_id = file[2]

                            await bot.forward_messages(entity=user.chat_id, messages=file_message_id,
                                                       from_peer=file_chat_id, drop_author=True)

                    except ValueError:
                        await bot.send_message(entity=user.chat_id, message=MessageText.BAD_FORMAT_SENT_ID,
                                               buttons=back_markup)

        del user

    elif type(chat) == Channel:
        pass


@bot.on(event=CallbackQuery)
async def my_event_handler(event: NewMessage.Event):
    data = event.data.decode()
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
            print(data)

        del user


bot.start()
bot.run_until_disconnected()
