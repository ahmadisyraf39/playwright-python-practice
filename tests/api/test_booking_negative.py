import pytest
from playwright.sync_api import APIRequestContext


@pytest.mark.parametrize("method", ["PUT", "PATCH", "DELETE"])
def test_change_without_token_is_forbidden(api: APIRequestContext, booking: dict, method: str):
    path = f"/booking/{booking['id']}"
    changed = {**booking["payload"], "firstname": "Hacker"}

    response = api.fetch(path, method=method, data=changed)    # no auth headers
    assert response.status == 403, f"{method} status {response.status}"

    # The booking must be untouched
    saved = api.get(path)
    assert saved.ok, f"booking disappeared after rejected {method}"
    assert saved.json() == booking["payload"]


def test_update_with_wrong_token_is_forbidden(api: APIRequestContext, booking: dict):
    path = f"/booking/{booking['id']}"
    changed = {**booking["payload"], "firstname": "Hacker"}

    response = api.put(path, data=changed, headers={"Cookie": "token=not-a-real-token"})
    assert response.status == 403, f"status {response.status}"

    assert api.get(path).json() == booking["payload"]


def test_get_unknown_booking_returns_404(api: APIRequestContext):
    response = api.get("/booking/999999999")
    assert response.status == 404, f"status {response.status}"


@pytest.mark.parametrize("missing_field", ["firstname", "totalprice", "bookingdates"])
@pytest.mark.xfail(reason="restful-booker returns 500 for invalid data; a correct API returns 400")
def test_create_with_missing_field_returns_400(api: APIRequestContext, booking_payload: dict, missing_field: str):
    invalid = {k: v for k, v in booking_payload.items() if k != missing_field}

    response = api.post("/booking", data=invalid)
    assert response.status == 400, f"status {response.status}"