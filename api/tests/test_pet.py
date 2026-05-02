import pytest
from api.data.payloads import pet_payload

@pytest.mark.api
class TestPet:
    def test_create_pet(self, pet_client):
        payload = pet_payload()
        r = pet_client.create(payload)
        assert r.status_code == 200
        body = r.json()
        assert body["id"] == payload["id"]
        assert body["status"] == "available"

    def test_get_pet_by_id(self, pet_client):
        created = pet_client.create(pet_payload()).json()
        r = pet_client.get(created["id"])
        assert r.status_code == 200
        assert r.json()["id"] == created["id"]

    def test_update_pet_status(self, pet_client):
        created = pet_client.create(pet_payload()).json()
        created["status"] = "sold"
        r = pet_client.update(created)
        assert r.status_code == 200
        assert r.json()["status"] == "sold"

    def test_find_by_status_available(self, pet_client):
        r = pet_client.find_by_status("available")
        assert r.status_code == 200
        assert isinstance(r.json(), list)

    def test_delete_pet(self, pet_client):
        created = pet_client.create(pet_payload()).json()
        r = pet_client.delete(created["id"])
        assert r.status_code == 200
        assert pet_client.get(created["id"]).status_code == 404

    def test_get_inexistent_pet_returns_404(self, pet_client):
        r = pet_client.get(999999999999)
        assert r.status_code == 404
