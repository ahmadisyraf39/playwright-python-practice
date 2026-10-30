import re
from playwright.sync_api import sync_playwright, expect, Page

def login(page: Page, username: str, password: str):
    page.goto("https://the-internet.herokuapp.com/login")
    page.get_by_label("Username").fill(username)
    page.get_by_label("Password").fill(password)
    page.get_by_role("button", name="Login").click()

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False, slow_mo=500)

    # Run 1: correct credentials
    context = browser.new_context()
    page = context.new_page()
    login(page, "tomsmith", "SuperSecretPassword!")
    expect(page).to_have_url(re.compile(r".*/secure$"))
    expect(page.get_by_text("You logged into a secure area!")).to_be_visible()
    context.close()

    # Run 2: wrong password
    context = browser.new_context()
    page = context.new_page()
    login(page, "tomsmith", "wrong-password")
    expect(page).to_have_url(re.compile(r".*/login$"))
    expect(page.get_by_text("Your password is invalid!")).to_be_visible()
    context.close()

    browser.close()