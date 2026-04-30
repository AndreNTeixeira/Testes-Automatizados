from .base_client import BaseClient

class UserClient(BaseClient):
    def create(self, payload: dict):
        return self.session.post(self._url("/user"), json=payload)

    def get(self, username: str):
        return self.session.get(self._url(f"/user/{username}"))

    def update(self, username: str, payload: dict):
        return self.session.put(self._url(f"/user/{username}"), json=payload)

    def delete(self, username: str):
        return self.session.delete(self._url(f"/user/{username}"))

    def login(self, username: str, password: str):
        return self.session.get(
            self._url("/user/login"),
            params={"username": username, "password": password},
        )

    def logout(self):
        return self.session.get(self._url("/user/logout"))
