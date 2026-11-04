from playwright.sync_api import APIRequestContext


def test_token_is_returned(token: str):
    # the fixture already did the work; check the token looks sensible
    # (a non-empty string)
    ...
    
    assert isinstance(token, str), f"token is not a string: {token!r}"
    assert token.strip(), "token is empty"



def test_bad_credentials_rejected(api: APIRequestContext):
    # POST /auth with a wrong password
    # What does the API actually return? Status code AND body
    ...

    response = api.post("/auth", data={"username": "admin", "password": "wrong-password"})
    body = response.json()

    assert response.status == 200, f"status {response.status}"
    assert "token" not in body, f"got a token with a wrong password: {body}"
    assert body.get("reason") == "Bad credentials", f"unexpected body: {body}"