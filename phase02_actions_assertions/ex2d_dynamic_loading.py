from playwright.sync_api import sync_playwright, expect, Page

def check_dynamic_loading(page: Page, url: str) -> None:

    page.goto(url)

    loading = page.locator("#loading")
    message = page.get_by_text("Hello World!")

    page.get_by_role("button", name="Start").click()

    expect(loading).to_be_visible()
    expect(loading).to_be_hidden(timeout=15_000)
    expect(message).to_be_visible()

    print(message.inner_text())

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    check_dynamic_loading(page, "https://the-internet.herokuapp.com/dynamic_loading/1")
    check_dynamic_loading(page, "https://the-internet.herokuapp.com/dynamic_loading/2")

    browser.close()

    