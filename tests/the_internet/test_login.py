import re
from playwright.sync_api import Page, expect

def login(page: Page, username: str, password: str) -> None:
    page.goto("https://the-internet.herokuapp.com/login")
    page.get_by_label("Username").fill(username)
    page.get_by_label("Password").fill(password)
    page.get_by_role("button", name="Login").click()


def test_valid_login(page: Page):
    # go to the login page, log in as tomsmith with the right password
    # assert the URL ends with /secure and the success message is visible
    login(page, "tomsmith", "SuperSecretPassword!")
    expect(page).to_have_url(re.compile(r".*/secure$"))
    expect(page.get_by_text("You logged into a secure area!")).to_be_visible()
       


def test_wrong_password(page: Page):
    # same, with a wrong password
    # assert you stay on /login and the error message is visible
    login(page, "tomsmith", "wrong-password")
    expect(page).to_have_url(re.compile(r".*/login$"))
    expect(page.get_by_text("Your password is invalid!")).to_be_visible()

def test_wrong_username(page: Page):
    login(page, "nobody", "SuperSecretPassword!")
    expect(page).to_have_url(re.compile(r".*/login$"))
    expect(page.get_by_text("Your username is invalid!")).to_be_visible()
        