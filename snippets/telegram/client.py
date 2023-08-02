from requests import Session, Response
from telegram_api import TelegramApi


class Client:
    def __init__(self, host):
        self.host = host
        self.session = Session()
        self.telegram = TelegramApi(host=self.host, session=self.session)
