from playwright.sync_api import sync_playwright, expect

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=500)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://uitestingplayground.com/classattr")

    # 1. Create a CSS locator for the blue (primary) button only
    locator = page.locator("button.btn-primary")

    # 2. Check exactly ONE element matches it      (hint: to_have_count)
    expect(locator).to_have_count(1)

    # 3. Register the dialog handler (above), THEN click the button
    messages = []

    def handle_dialog(dialog):            
        messages.append(dialog.message)   
        dialog.accept()              

    page.once("dialog", handle_dialog)
    locator.click()     

    # 4. Assert the alert message was captured, and print it
    #    (a plain assert on the messages list)
    assert messages, "no alert appeared"
    print(messages[0])

    browser.close()