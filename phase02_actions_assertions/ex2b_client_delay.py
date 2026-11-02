from playwright.sync_api import sync_playwright, expect

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("http://uitestingplayground.com/clientdelay")

    button = page.get_by_role("button", name="Button Triggering Client Side Logic")
    messages = page.get_by_text("Data calculated on the client side.")

    # Part 1: one click -> one message
    button.click()
    expect(messages).to_have_count(1, timeout=20_000)
    print("Part 1:", messages.inner_text())

    # Part 2: two clicks -> two messages (calculations run one after another)
    page.reload()
    button.click()
    button.click()
    expect(messages).to_have_count(2, timeout=40_000)
    for message in messages.all():
        print("Part 2:", message.inner_text())

    browser.close()