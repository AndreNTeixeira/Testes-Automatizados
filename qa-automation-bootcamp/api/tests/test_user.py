import pytest
from api.data.payloads import user_payload

@pytest.mark.api
class TestUser:
    def test_create_user(self, user_client):
        payload = user_payload()
        r = user_client.create(payload)
        assert r.status_code == 200

    def test_get_user(self, user_client):
        payload = user_payload()
        user_client.create(payload)
        r = user_client.get(payload["username"])
        assert r.status_code == 200
        assert r.json()["username"] == payload["username"]

    def test_update_user(self, user_client):
        payload = user_payload()
        user_client.create(payload)
        payload["firstName"] = "Atualizado"
        r = user_client.update(payload["username"], payload)
        assert r.status_code == 200

    def test_login_logout(self, user_client):
        payload = user_payload()
        user_client.create(payload)
        login = user_client.login(payload["username"], payload["password"])
        assert login.status_code == 200
        assert user_client.logout().status_code == 200

    def test_delete_user(self, user_client):
        payload = user_payload()
        user_client.create(payload)
        r = user_client.delete(payload["username"])
        assert r.status_code == 200
