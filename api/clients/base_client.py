import requests

class BaseClient:
    BASE_URL = "https://petstore.swagger.io/v2"

    def __init__(self, session: requests.Session):
        self.session = session

    def _url(self, path: str) -> str:
        return f"{self.BASE_URL}{path}"
