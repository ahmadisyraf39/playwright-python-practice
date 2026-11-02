from playwright.sync_api import sync_playwright, expect

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("http://uitestingplayground.com/ajax")

    # 1. Click the "Button Triggering AJAX Request" button
    page.get_by_role("button", name="Button Triggering AJAX Request").click()

    # 2. Check the message "Data loaded with AJAX get request." appears
    #    No sleep, no wait_for_timeout
    message = page.get_by_text("Data loaded with AJAX get request.")
    expect(message).to_be_visible(timeout=20_000)

    # 3. Print the message text
    print(message.inner_text())

    browser.close()