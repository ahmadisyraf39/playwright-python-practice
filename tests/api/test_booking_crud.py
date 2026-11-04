from playwright.sync_api import APIRequestContext


def test_create_and_read_booking(api: APIRequestContext, auth_headers: dict, booking_payload: dict):
    response = api.post("/booking", data=booking_payload)
    assert response.ok, f"status {response.status}: {response.text()}"

    body = response.json()
    booking_id = body.get("bookingid")
    assert booking_id, f"no bookingid in response: {body}"

    try:
        assert body["booking"] == booking_payload           # create echoes the saved data

        read = api.get(f"/booking/{booking_id}")
        assert read.ok, f"status {read.status}"
        assert read.json() == booking_payload               # GET returns the same data
    finally:
        api.delete(f"/booking/{booking_id}", headers=auth_headers)   # cleanup, even on failure


def test_update_booking(api: APIRequestContext, booking: dict, auth_headers: dict):
    updated = {**booking["payload"], "firstname": "Isyraf", "totalprice": 200}

    response = api.put(f"/booking/{booking['id']}", data=updated, headers=auth_headers)
    assert response.ok, f"status {response.status}"

    saved = api.get(f"/booking/{booking['id']}").json()
    assert saved == updated


def test_partial_update_booking(api: APIRequestContext, booking: dict, auth_headers: dict):
    response = api.patch(
        f"/booking/{booking['id']}",
        data={"additionalneeds": "Futsal court"},
        headers=auth_headers,
    )
    assert response.ok, f"status {response.status}"

    saved = api.get(f"/booking/{booking['id']}").json()
    assert saved["additionalneeds"] == "Futsal court"

    expected = {**booking["payload"], "additionalneeds": "Futsal court"}
    assert saved == expected                 # every OTHER field unchanged


def test_delete_booking(api: APIRequestContext, booking: dict, auth_headers: dict):
    response = api.delete(f"/booking/{booking['id']}", headers=auth_headers)
    assert response.status == 201, f"status {response.status}"   # restful-booker quirk

    gone = api.get(f"/booking/{booking['id']}")
    assert gone.status == 404, f"status {gone.status}"