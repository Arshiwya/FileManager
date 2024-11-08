import sys

from telethon import events
from telethon.events.newmessage import NewMessage
from telethon.events.callbackquery import CallbackQuery
from telethon.types import User, Channel, MessageMediaPhoto, MessageMediaDocument, Message, InputDocument, InputPhoto
from telethon.errors.rpcerrorlist import MediaEmptyError
from config import bot

from functions import get_user, sign_user, change_step, add_file, delete_file, get_user_files, get_file, set_file_type, \
    get_file_uploader, change_file_status, get_file_status, set_file_title, add_one_download_to_file, get_file_downloads
from keyboards import home_markup, tos_markup, back_markup, make_manage_inline_markup, make_manage_panel_inline_markup, \
    make_delete_panel_inline_markup, make_edit_title_panel_inline_markup
from reports import Report, ErrorReport, ReportCode
from messages import MessageText
from models import MyUser, Step, Link, TextOperationPrefix, StepPrefix, Button, CallBackQueryPrefix, CallBackQuery


@bot.on(event=NewMessage)
async def main_handler(event: NewMessage.Event):
    text = event.raw_text
    chat = event.chat
    message = event.message

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

            if (text == '/start' and user.step != Step.TOS) or (user.step == Step.HOME and text == Button.BACK):
                change_step(user=user, step=Step.HOME)
                await bot.send_message(entity=user.chat_id, message=MessageText.WELLCOME.format(name=user.name),
                                       buttons=home_markup)

            elif TextOperationPrefix.DOWNLOAD_FILE in text:
                file_rowid = TextOperationPrefix.get_file_rowid(prefix=TextOperationPrefix.DOWNLOAD_FILE, text=text)
                file = get_file(file_rowid=file_rowid)

                if file is None:
                    await bot.send_message(entity=user.chat_id, message=MessageText.FILE_NOT_FOUND,
                                           buttons=home_markup)

                else:
                    file_id = file[0]
                    access_hash = int(file[2])
                    file_reference = file[3]
                    file_type = file[4]
                    status = file[5]
                    title = file[6]
                    downloads = file[7]
                    if title != "" and title is not None:
                        title = MessageText.FILE_MESSAGE_STRUCTURE.format(title=title, downloads=downloads)

                    else:
                        title = MessageText.FILE_MESSAGE_STRUCTURE.format(title="Not set", downloads=downloads)

                    uploader = get_file_uploader(rowid=file_rowid)
                    if status == 1:

                        if file_type == 'image':
                            image = InputPhoto(id=file_id, access_hash=access_hash,
                                               file_reference=file_reference)
                            await bot.send_file(entity=user.chat_id, file=image,
                                                caption=title)

                        elif file_type == 'doc':
                            file = InputDocument(id=file_id, access_hash=access_hash,
                                                 file_reference=file_reference)
                            await bot.send_file(entity=user.chat_id, file=file,
                                                caption=title)

                        if uploader != user.chat_id:
                            add_one_download_to_file(file_rowid=file_rowid)

                    else:
                        if uploader == user.chat_id:

                            if file_type == 'image':
                                image = InputPhoto(id=file_id, access_hash=access_hash,
                                                   file_reference=file_reference)
                                await bot.send_file(entity=user.chat_id, file=image,
                                                    caption=title)

                            elif file_type == 'doc':
                                file = InputDocument(id=file_id, access_hash=access_hash,
                                                     file_reference=file_reference)
                                await bot.send_file(entity=user.chat_id, file=file,
                                                    caption=title)

                            await bot.send_message(entity=user.chat_id, message=MessageText.FILE_IS_DRAFT_OWNER_TEXT)

                        else:
                            await bot.send_message(entity=user.chat_id, message=MessageText.FILE_IS_DRAFT)

            elif StepPrefix.SETTING_TITLE_FOR_FILE in str(user.step):
                if text == Button.BACK:
                    change_step(user=user, step=Step.HOME)
                    await bot.send_message(entity=user.chat_id, message=MessageText.WELLCOME.format(name=user.name),
                                           buttons=home_markup)

                else:
                    file_rowid = StepPrefix.get_file_rowid(prefix=StepPrefix.SETTING_TITLE_FOR_FILE, step=user.step)

                    if len(text) > 60:
                        await bot.send_message(entity=user.chat_id, message=MessageText.TOO_LONG_TITLE)
                    else:
                        change_step(user=user, step=Step.HOME)
                        set_file_title(file_rowid=file_rowid, title=text)
                        await bot.send_message(entity=user.chat_id, message=MessageText.TITLE_SET, buttons=home_markup)

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
                            markup = make_manage_inline_markup(rowid=rowid)

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

                            markup = make_manage_inline_markup(rowid=rowid)

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
                        file = get_file(file_rowid=rowid)

                        if file is None:
                            await bot.send_message(entity=user.chat_id, message=MessageText.FILE_NOT_FOUND,
                                                   buttons=back_markup)

                        else:
                            uploader = get_file_uploader(rowid=rowid)
                            if uploader == user.chat_id:
                                file_id = file[0]
                                access_hash = int(file[2])
                                file_reference = file[3]
                                file_type = file[4]
                                status = file[5]
                                title = file[6]
                                downloads = file[7]
                                if title != "" and title is not None:
                                    title = MessageText.FILE_MESSAGE_STRUCTURE.format(title=title, downloads=downloads)

                                markup = make_manage_panel_inline_markup(rowid=rowid, status=status,
                                                                         downloads=downloads)

                                if file_type == 'image':
                                    image = InputPhoto(id=file_id, access_hash=access_hash,
                                                       file_reference=file_reference)
                                    # caption = await bot.get_messages(caption[0], ids=caption[1])
                                    # print(caption)
                                    await bot.send_file(entity=user.chat_id, file=image, caption=title, buttons=markup)

                                elif file_type == 'doc':
                                    file = InputDocument(id=file_id, access_hash=access_hash,
                                                         file_reference=file_reference)
                                    await bot.send_file(entity=user.chat_id, file=file, caption=title, buttons=markup)

                                else:
                                    try:
                                        file = InputPhoto(id=file_id, access_hash=access_hash,
                                                          file_reference=file_reference)
                                        sent_file = await bot.send_file(entity=user.chat_id, file=file, caption=None)
                                        set_file_type(file_id=file_id, file_type='image')

                                    except MediaEmptyError as error:
                                        file = InputDocument(id=file_id, access_hash=access_hash,
                                                             file_reference=file_reference)
                                        sent_file = await bot.send_file(entity=user.chat_id, file=file, caption=None)
                                        set_file_type(file_id=file_id, file_type='doc')

                            else:
                                await bot.send_message(entity=user.chat_id, message=MessageText.FILE_NOT_FOUND,
                                                       buttons=back_markup)

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

            if data == CallBackQuery.CLOSE_PANEL:
                await bot.edit_message(entity=user.chat_id, message=message, text=MessageText.PANEL_CLOSED,
                                       buttons=None)

            elif StepPrefix.EDITING_TITLE in str(user.step) and data == CallBackQuery.BACK_TO_MANAGE:
                file_rowid = StepPrefix.get_file_rowid(prefix=StepPrefix.EDITING_TITLE, step=user.step)
                change_step(user=user, step=Step.HOME)
                status = get_file_status(file_rowid=file_rowid)
                downloads = get_file_downloads(file_rowid=file_rowid)
                markup = make_manage_panel_inline_markup(rowid=file_rowid, status=status, downloads=downloads)
                await bot.edit_message(entity=user.chat_id, message=message, buttons=markup)

            elif data == CallBackQuery.NULL:
                message = MessageText.WRONG_INLINE_INPUT
                await event.answer(message=message)

            elif CallBackQueryPrefix.MANAGE in data:

                if StepPrefix.CONFIRM_DELETE_FILE in str(user.step):
                    change_step(user=user, step=Step.HOME)

                prefix = CallBackQueryPrefix.MANAGE
                file_rowid = CallBackQueryPrefix.get_file_rowid(prefix=prefix, data=data)
                status = get_file_status(file_rowid=file_rowid)
                downloads = get_file_downloads(file_rowid=file_rowid)
                markup = make_manage_panel_inline_markup(rowid=file_rowid, status=status, downloads=downloads)
                await bot.edit_message(entity=user.chat_id, message=message, buttons=markup)

            elif CallBackQueryPrefix.EDITE_FILE_TITLE in data:
                prefix = CallBackQueryPrefix.EDITE_FILE_TITLE
                file_rowid = CallBackQueryPrefix.get_file_rowid(prefix=prefix, data=data)

                file_uploader = get_file_uploader(rowid=file_rowid)

                if file_uploader is None:
                    await event.answer(message=MessageText.FILE_HAS_PRIVACY_PROBLEM, alert=True)
                    delete_file(file_rowid)

                else:
                    uploader = file_uploader

                    if user.chat_id == int(uploader):
                        change_step(user=user, step=(StepPrefix.EDITING_TITLE + file_rowid))
                        markup = make_edit_title_panel_inline_markup(rowid=file_rowid)
                        await bot.edit_message(entity=user.chat_id, message=message, buttons=markup)
                    else:
                        await event.answer(message=MessageText.ACCESS_DENIED_WARNING, alert=True)

            elif CallBackQueryPrefix.DELETE_FILE_TITLE in data:
                file_rowid = CallBackQueryPrefix.get_file_rowid(prefix=CallBackQueryPrefix.DELETE_FILE_TITLE, data=data)
                set_file_title(file_rowid=file_rowid, title='')
                status = get_file_status(file_rowid=file_rowid)
                downloads = get_file_downloads(file_rowid=file_rowid)
                markup = make_manage_panel_inline_markup(rowid=file_rowid, status=status, downloads=downloads)
                await event.answer(message=MessageText.FILE_UPDATED, alert=True)
                await bot.edit_message(entity=user.chat_id, message=message, text="", buttons=markup)

            elif CallBackQueryPrefix.SET_FILE_TITLE in data:
                file_rowid = CallBackQueryPrefix.get_file_rowid(prefix=CallBackQueryPrefix.SET_FILE_TITLE, data=data)
                change_step(user=user, step=StepPrefix.SETTING_TITLE_FOR_FILE + file_rowid)
                await bot.send_message(entity=user.chat_id, message=MessageText.SEND_DESIRE_TITLE, buttons=back_markup)

            elif CallBackQueryPrefix.DELETE_FILE in data:
                file_rowid = CallBackQueryPrefix.get_file_rowid(prefix=CallBackQueryPrefix.DELETE_FILE, data=data)
                change_step(user=user, step=(StepPrefix.CONFIRM_DELETE_FILE + file_rowid))
                markup = make_delete_panel_inline_markup(rowid=file_rowid)
                await bot.edit_message(entity=user.chat_id, message=message, buttons=markup)

            elif CallBackQueryPrefix.KILL_FILE in data:
                file_rowid = CallBackQueryPrefix.get_file_rowid(prefix=CallBackQueryPrefix.KILL_FILE, data=data)
                change_step(user=user, step=Step.HOME)
                delete_file(rowid=file_rowid)
                await bot.edit_message(entity=user.chat_id, message=message, buttons=None,
                                       text=MessageText.FILE_DELETED)
                await bot.send_message(entity=user.chat_id, message=MessageText.WELLCOME.format(name=user.name),
                                       buttons=home_markup)

            elif CallBackQueryPrefix.ACTIVE_STATUS in data:
                file_rowid = CallBackQueryPrefix.get_file_rowid(prefix=CallBackQueryPrefix.ACTIVE_STATUS, data=data)
                change_file_status(file_rowid=file_rowid, status=1)
                downloads = get_file_downloads(file_rowid=file_rowid)
                markup = make_manage_panel_inline_markup(rowid=file_rowid, status=1, downloads=downloads)
                await event.answer(message=MessageText.FILE_UPDATED, alert=True)
                await bot.edit_message(entity=user.chat_id, message=message, buttons=markup)

            elif CallBackQueryPrefix.DEACTIVATE_STATUS in data:
                file_rowid = CallBackQueryPrefix.get_file_rowid(prefix=CallBackQueryPrefix.DEACTIVATE_STATUS, data=data)
                change_file_status(file_rowid=file_rowid, status=0)
                downloads = get_file_downloads(file_rowid=file_rowid)
                markup = make_manage_panel_inline_markup(rowid=file_rowid, status=0, downloads=downloads)
                await event.answer(message=MessageText.FILE_UPDATED, alert=True)
                await bot.edit_message(entity=user.chat_id, message=message, buttons=markup)

            elif CallBackQueryPrefix.DOWNLOAD_LINK in data:
                file_rowid = CallBackQueryPrefix.get_file_rowid(prefix=CallBackQueryPrefix.DOWNLOAD_LINK, data=data)
                dl = Link.DOWNLOAD_FILE.format(rowid=file_rowid)
                message = MessageText.DOWNLOAD_LINK.format(rowid=file_rowid, link=dl)
                await bot.send_message(entity=user.chat_id, message=message)

        del user


bot.start()
bot.run_until_disconnected()
