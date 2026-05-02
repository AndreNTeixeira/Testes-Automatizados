import pytest
from api.data.payloads import order_payload, pet_payload

@pytest.mark.api
class TestStore:
    def test_place_order(self, store_client, pet_client):
        pet = pet_client.create(pet_payload()).json()
        r = store_client.place_order(order_payload(pet["id"]))
        assert r.status_code == 200
        assert r.json()["status"] == "placed"

    def test_get_order(self, store_client, pet_client):
        pet = pet_client.create(pet_payload()).json()
        order = store_client.place_order(order_payload(pet["id"])).json()
        r = store_client.get_order(order["id"])
        assert r.status_code == 200
        assert r.json()["id"] == order["id"]

    def test_delete_order(self, store_client, pet_client):
        pet = pet_client.create(pet_payload()).json()
        order = store_client.place_order(order_payload(pet["id"])).json()
        r = store_client.delete_order(order["id"])
        assert r.status_code == 200

    def test_inventory(self, store_client):
        r = store_client.inventory()
        assert r.status_code == 200
        assert isinstance(r.json(), dict)
