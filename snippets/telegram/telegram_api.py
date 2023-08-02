from base_api import BaseApi
from models import SendMessage

TOKEN = ''
CHAT_ID = ''


class TelegramApi(BaseApi):
    def send_message(self, message):
        self.url.path.segments = [TOKEN, 'sendMessage']
        self.url.args = {'chat_id': CHAT_ID, 'text': message}
        return SendMessage(**self.session.get(self.url).json())
