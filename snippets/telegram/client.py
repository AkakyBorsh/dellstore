from requests import Session
from snippets.telegram.telegram_api import TelegramApi

TOKEN = ''
HOST = ''
CHAT_ID = ''


class Client:
    def __init__(self, host):
        self.host = host
        self.session = Session()
        self.telegram = TelegramApi(host=self.host, session=self.session)
