from playwright.sync_api import sync_playwright, expect

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False, slow_mo=500)
    page = browser.new_page()
    page.goto("https://the-internet.herokuapp.com/login")

    # 1. Fill the username field
    page.get_by_label("Username").fill("tomsmith")

    # 2. Fill the password field
    page.get_by_label("Password").fill("SuperSecretPassword!")

    # 3. Click the Login button
    page.get_by_role("button", name="Login").click()

    # 4. Check you landed on the secure page (URL ends with /secure)
    page.wait_for_url("https://the-internet.herokuapp.com/secure")

    # 5. Check the success message "You logged into a secure area!" is shown
    page.get_by_text("You logged into a secure area")

    browser.close()