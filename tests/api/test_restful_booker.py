from playwright.sync_api import APIRequestContext


def test_get_bookings(api: APIRequestContext):
    response = api.get("/booking")

    assert response.ok, f"status {response.status}"
    bookings = response.json()
    assert len(bookings) > 0
    assert "bookingid" in bookings[0]

def test_ping(api: APIRequestContext):
    response = api.get("/ping")

    assert response.ok, f"status {response.status}"
    assert response.status == 201

def test_get_booking_by_id(api: APIRequestContext):
    
    bookings = api.get("/booking").json()
    assert bookings, "no bookings available"
    booking_id = bookings[0]["bookingid"]

    response = api.get(f"/booking/{booking_id}")
    assert response.ok, f"status {response.status}"

    body = response.json()

    for key in ["firstname", "lastname", "totalprice", "depositpaid", "bookingdates"]:
        assert key in body, f"missing key: {key}"

    for key in ["checkin", "checkout"]:
        assert key in body["bookingdates"], f"missing bookingdates key: {key}"

    