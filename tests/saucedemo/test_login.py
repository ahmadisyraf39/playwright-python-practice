import re
import pytest
from playwright.sync_api import Page, expect

LOGIN_URL = "https://www.saucedemo.com/"

@pytest.mark.parametrize("username, should_succeed", [
    # one tuple per user from the table above
    ("standard_user", True),
    ("locked_out_user", False),
    ("problem_user", True),
    ("performance_glitch_user", True),
])

def test_login(page: Page, username: str, should_succeed: bool):
    # 1. Go to saucedemo and log in with username + "secret_sauce"
    page.goto(LOGIN_URL)
    page.get_by_placeholder("Username").fill(username)
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.get_by_role("button", name="Login").click()

    # 2. If should_succeed:
    #       assert you're on the inventory page
    #    Else:
    #       assert you're still on the login page
    #       assert the locked-out error message is visible
    if should_succeed:
       expect(page).to_have_url(re.compile(r".*/inventory\.html$"), timeout=10_000)
    else:
        expect(page).to_have_url(LOGIN_URL)
        expect(page.get_by_text("Sorry, this user has been locked out")).to_be_visible()