import pytest
import requests
from api.clients.user_client import UserClient
from api.clients.store_client import StoreClient
from api.clients.pet_client import PetClient

@pytest.fixture(scope="session")
def http():
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json", "Accept": "application/json"})
    yield s
    s.close()

@pytest.fixture
def user_client(http): return UserClient(http)

@pytest.fixture
def store_client(http): return StoreClient(http)

@pytest.fixture
def pet_client(http): return PetClient(http)
