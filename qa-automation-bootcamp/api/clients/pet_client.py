from .base_client import BaseClient

class PetClient(BaseClient):
    def create(self, payload: dict):
        return self.session.post(self._url("/pet"), json=payload)

    def get(self, pet_id: int):
        return self.session.get(self._url(f"/pet/{pet_id}"))

    def update(self, payload: dict):
        return self.session.put(self._url("/pet"), json=payload)

    def delete(self, pet_id: int):
        return self.session.delete(self._url(f"/pet/{pet_id}"))

    def find_by_status(self, status: str):
        return self.session.get(
            self._url("/pet/findByStatus"), params={"status": status}
        )
