from secret import bot_username


class MyUser:
    chat_id = None
    name = None
    step = None

    def __init__(self, chat_id, name, step):
        self.chat_id = chat_id
        self.name = name
        self.step = step


class Step:
    TOS = 0
    HOME = 10
    SENDING_FILE = 11
    SENDING_FILE_ID_FOR_MANAGE = 12


class Button:
    BACK = "back 🔙"
    ADD_FILE = "Add file ➕"
    SEARCH_FILE = "Search file 🔍"
    MY_FILE = "My files 🗃"
    MANAGE_FILE = "Manage files ⚙️"
    ACCEPT_TOS = 'I read and accept ✅'
    REJECT_TOS = "I don't accept ❌"


class StepPrefix:
    MANAGING_FILE = "managing-"
    CONFIRM_DELETE_FILE = "delete-"

    @classmethod
    def get_file_rowid(cls, prefix: str, step: str):
        splits = step.split(sep=prefix)
        file_rowid = splits[1]

        return file_rowid


class CallBackQuery:
    NULL = 'null'
    CLOSE_PANEL = 'close-panel'


class CallBackQueryPrefix:
    MANAGE = "manage-"
    SET_FILE_TITLE = 'title-'
    DELETE_FILE = 'delete-'
    KILL_FILE = 'kill-'
    ACTIVE_STATUS = 'status+'
    DEACTIVATE_STATUS = 'status-'
    DOWNLOAD_LINK = 'dllink-'

    @classmethod
    def get_file_rowid(cls, prefix: str, data: str):
        splits = data.split(sep=prefix)
        file_rowid = splits[1]

        return file_rowid


class TextOperationPrefix:
    DOWNLOAD_FILE = 'dl_'

    @classmethod
    def get_file_rowid(cls, prefix: str, text: str):
        splits = text.split(sep=prefix)
        file_rowid = splits[1]

        return file_rowid


class Link:
    DOWNLOAD_FILE = f'https://telegram.me/{bot_username}?start={TextOperationPrefix.DOWNLOAD_FILE}' + '{rowid}'
