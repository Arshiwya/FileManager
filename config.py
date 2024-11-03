from telethon import TelegramClient
from secret import api_id, api_hash, bot_token

bot = TelegramClient('Telethoning', api_id, api_hash).start(bot_token=bot_token)
