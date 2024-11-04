import sys

from telethon import events
from telethon.events.newmessage import NewMessage
from telethon.events.callbackquery import CallbackQuery
from telethon.types import User, Channel, MessageMediaPhoto, MessageMediaDocument, Message, InputDocument, InputPhoto
from config import bot

from functions import get_user, sign_user, change_step, add_file, get_user_files, get_file
from keyboards import home_markup, tos_markup, back_markup, make_manage_inline_markup, make_manage_panel_inline_markup
from reports import Report, ErrorReport, ReportCode
from messages import MessageText
from models import MyUser, Step, Button, CallBackQueryPrefix, CallBackQuery


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
            if text == '/start' and user.step != Step.TOS:
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
                            file_id = event.media.photo.id
                            access_hash = event.media.photo.access_hash
                            file_reference = event.media.photo.file_reference

                            image = InputPhoto(id=file_id, access_hash=access_hash, file_reference=file_reference)

                            file_reference = str(event.media.photo.file_reference)

                            rowid = add_file(file_id=file_id, access_hash=access_hash, file_reference=file_reference,
                                             file_type='image', uploader=user.chat_id)
                            markup = make_manage_inline_markup(file_id=rowid)

                            await bot.send_file(entity=user.chat_id, file=image,
                                                caption=MessageText.IMAGE_FILE_SAVED.format(file_id=rowid),
                                                buttons=markup)
                            await bot.send_message(entity=user.chat_id,
                                                   message=MessageText.WELLCOME.format(name=user.name),
                                                   buttons=home_markup)

                        elif type(event.media) == MessageMediaDocument:
                            change_step(user=user, step=Step.HOME)
                            file_id = event.media.document.id
                            access_hash = event.media.document.access_hash
                            file_reference = event.media.document.file_reference

                            file = InputDocument(id=file_id, access_hash=access_hash, file_reference=file_reference)

                            file_reference = str(event.media.document.file_reference)

                            rowid = add_file(file_id=file_id, access_hash=access_hash, file_reference=file_reference,
                                             file_type='doc', uploader=user.chat_id)

                            markup = make_manage_inline_markup(file_id=rowid)

                            await bot.send_file(entity=user.chat_id, file=file,
                                                caption=MessageText.FILE_SAVED.format(file_id=rowid),
                                                buttons=markup)
                            await bot.send_message(entity=user.chat_id,
                                                   message=MessageText.WELLCOME.format(name=user.name),
                                                   buttons=home_markup)

                    elif type(event) == NewMessage.Event and not event.media:
                        await bot.send_message(entity=user.chat_id,
                                               message=MessageText.TEXT_MESSAGE_NOT_SUPPORT_FOR_FILE,
                                               buttons=back_markup)

            elif user.step == Step.SENDING_FILE_ID_FOR_MANAGE:
                if text == Button.BACK:
                    change_step(user=user, step=Step.HOME)
                    await bot.send_message(entity=user.chat_id, message=MessageText.WELLCOME.format(name=user.name),
                                           buttons=home_markup)

                else:
                    try:
                        rowid = int(text)
                        file = get_file(rowid)

                        if file is None:
                            await bot.send_message(entity=user.chat_id, message=MessageText.FILE_NOT_FOUND,
                                                   buttons=back_markup)

                        else:
                            file_id = file[0]
                            access_hash = int(file[2])
                            file_reference = file[3]
                            file_type = file[4]

                            if file_type == 'image':
                                image = InputPhoto(id=file_id, access_hash=access_hash, file_reference=file_reference)
                                await bot.send_file(entity=user.chat_id, file=image, caption=None)

                            elif file_type == 'doc':
                                file = InputDocument(id=file_id, access_hash=access_hash, file_reference=file_reference)
                                await bot.send_file(entity=user.chat_id, file=file, caption=None)

                    except ValueError:
                        await bot.send_message(entity=user.chat_id, message=MessageText.BAD_FORMAT_SENT_ID,
                                               buttons=back_markup)

        del user

    elif type(chat) == Channel:
        pass


@bot.on(event=CallbackQuery)
async def my_event_handler(event: CallbackQuery.Event):
    data = event.data.decode()
    chat = event.chat
    message: Message = await event.get_message()
    print(data)

    # if type(chat) == User:
    #
    #     user = get_user(chat)
    #
    #     if user is None:
    #         operation = sign_user(chat)
    #
    #         if operation.status_code == ReportCode.SUCCESS:
    #             await bot.send_message(entity=chat.id, message=MessageText.SUCCESS_SIGN_IN)
    #         else:
    #             await bot.send_message(entity=chat.id, message=MessageText.SIMPLE_ERROR)
    #
    #     else:
    #         user: MyUser
    #         if data == CallBackQuery.CLOSE_PANEL:
    #             await bot.edit_message(entity=user.chat_id, message=message, text=MessageText.PANEL_CLOSED,
    #                                    buttons=None)
    #         elif CallBackQueryPrefix.MANAGE in data:
    #             prefix = CallBackQueryPrefix.MANAGE
    #             file_id = CallBackQueryPrefix.get_file_id(prefix=prefix, data=data)
    #             markup = make_manage_panel_inline_markup(file_id)
    #
    #             await bot.edit_message(entity=user.chat_id, message=message, buttons=markup)
    #
    #     del user


bot.start()
bot.run_until_disconnected()
