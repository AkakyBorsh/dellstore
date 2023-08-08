import os
from snippets.telegram.base_api import BaseApi
from snippets.telegram.models import SendMessage

TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')


class TelegramApi(BaseApi):
    def send_message(self, message, token, chat_id):
        self.url.path.segments = [TELEGRAM_TOKEN, 'sendMessage']
        self.url.args = {'chat_id': TELEGRAM_CHAT_ID, 'text': message}
        return SendMessage(**self.session.get(self.url).json())
