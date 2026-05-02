from .base_client import BaseClient

class StoreClient(BaseClient):
    def place_order(self, payload: dict):
        return self.session.post(self._url("/store/order"), json=payload)

    def get_order(self, order_id: int):
        return self.session.get(self._url(f"/store/order/{order_id}"))

    def delete_order(self, order_id: int):
        return self.session.delete(self._url(f"/store/order/{order_id}"))

    def inventory(self):
        return self.session.get(self._url("/store/inventory"))
