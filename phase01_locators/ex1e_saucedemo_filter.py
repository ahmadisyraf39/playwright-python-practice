from playwright.sync_api import sync_playwright, expect

with sync_playwright() as p:

    p.selectors.set_test_id_attribute("data-test")

    browser = p.chromium.launch(headless=False, slow_mo=500)
    page = browser.new_page()
    page.goto("https://www.saucedemo.com/")

    # 1. Log in (inputs have no <label>: which get_by_* fits?)
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.locator("#login-button").click()

    # 2. Check you're on the inventory page
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")

    # 3. Locate ALL product cards
    cards = page.get_by_test_id("inventory-item")

    # 4. Check there are 6
    expect(cards).to_have_count(6)

    # 5. Filter the cards down to one product
    bike_light = cards.filter(has_text="Sauce Labs Bike Light")
    expect(bike_light).to_have_count(1)

    # 6. Inside that card, click its "Add to cart" button
    bike_light.get_by_role("button", name="Add to cart").click()

    # 7. The same card's button now says "Remove"
    expect(bike_light.get_by_role("button", name="Remove")).to_be_visible()

    # 8. Cart badge shows "1"
    expect(page.get_by_test_id("shopping-cart-badge")).to_have_text("1")

    # browser.close()