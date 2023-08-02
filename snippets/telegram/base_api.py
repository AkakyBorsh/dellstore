from requests import Session
from furl import furl


class BaseApi:
    def __init__(self, host: str, session: Session):
        self.host = host
        self.session = session
        self.url = furl(host)
