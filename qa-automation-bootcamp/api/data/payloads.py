import time

def unique_id() -> int:
    return int(time.time() * 1000)

def pet_payload(pet_id: int | None = None) -> dict:
    return {
        "id": pet_id or unique_id(),
        "name": "Rex",
        "category": {"id": 1, "name": "Dogs"},
        "photoUrls": ["https://example.com/rex.png"],
        "tags": [{"id": 1, "name": "vaccinated"}],
        "status": "available",
    }

def user_payload(username: str | None = None) -> dict:
    uname = username or f"user_{unique_id()}"
    return {
        "id": unique_id(),
        "username": uname,
        "firstName": "Andre",
        "lastName": "Tester",
        "email": f"{uname}@test.io",
        "password": "Pass123!",
        "phone": "11999999999",
        "userStatus": 1,
    }

def order_payload(pet_id: int) -> dict:
    return {
        "id": unique_id(),
        "petId": pet_id,
        "quantity": 1,
        "shipDate": "2026-05-01T12:00:00.000Z",
        "status": "placed",
        "complete": True,
    }
