from requests import Session
from snippets.telegram.telegram_api import TelegramApi


class Client:
    def __init__(self):
        self.session = Session()
        self.telegram = TelegramApi(host='https://api.telegram.org/', session=self.session)
