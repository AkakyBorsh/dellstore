from snippets.telegram.base_api import BaseApi
from snippets.telegram.models import SendMessage


class TelegramApi(BaseApi):
    def send_message(self, message, token, chat_id):
        self.url.path.segments = [token, 'sendMessage']
        self.url.args = {'chat_id': chat_id, 'text': message}
        return SendMessage(**self.session.get(self.url).json())
