import pytest
from playwright.sync_api import Playwright, APIRequestContext

BASE_URL = "https://restful-booker.herokuapp.com"


@pytest.fixture(scope="session")
def api(playwright: Playwright):
    context = playwright.request.new_context(base_url=BASE_URL)
    yield context          # the tests run here
    context.dispose()      # always runs afterwards, even if tests failed

@pytest.fixture(scope="session")
def token(api: APIRequestContext) -> str:
    # 1. POST /auth with the admin credentials from the docs
    response = api.post("/auth", data={"username": "admin", "password": "password123"})

    # 2. Assert the response is OK
    assert response.ok, f"status {response.status}"

    # 3. Read the token from the JSON body
    body = response.json()
    token = body.get("token")

    # 4. Assert a token was actually returned (not missing or empty)
    assert token, f"no token in response: {body}"

    # 5. Return it
    return token

@pytest.fixture(scope="session")
def auth_headers(token: str) -> dict:
    return {"Cookie": f"token={token}"}


@pytest.fixture
def booking_payload() -> dict:
    """Fresh booking data for each test (tests can change it safely)."""
    return {
        "firstname": "Ahmad",
        "lastname": "Isyraf",
        "totalprice": 120,
        "depositpaid": True,
        "bookingdates": {"checkin": "2026-12-01", "checkout": "2026-12-02"},
        "additionalneeds": "Badminton court",
    }


@pytest.fixture
def booking(api: APIRequestContext, auth_headers: dict, booking_payload: dict):
    """Create a booking for one test, and delete it afterwards."""
    response = api.post("/booking", data=booking_payload)
    assert response.ok, f"create failed: {response.status} {response.text()}"
    booking_id = response.json()["bookingid"]

    yield {"id": booking_id, "payload": booking_payload}

    api.delete(f"/booking/{booking_id}", headers=auth_headers)   # cleanup