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
