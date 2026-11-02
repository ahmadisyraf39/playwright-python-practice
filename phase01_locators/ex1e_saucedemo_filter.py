from playwright.sync_api import sync_playwright, expect, Page


def add_to_cart(page: Page, product_name: str) -> None:
    """Find a product card by its exact name and click its Add to cart button."""
    cards = page.get_by_test_id("inventory-item")
    card = cards.filter(has=page.get_by_text(product_name, exact=True))
    expect(card).to_have_count(1)
    card.get_by_role("button", name="Add to cart").click()
    expect(card.get_by_role("button", name="Remove")).to_be_visible()


with sync_playwright() as p:
    p.selectors.set_test_id_attribute("data-test")

    browser = p.chromium.launch(headless=False, slow_mo=500)
    page = browser.new_page()
    page.goto("https://www.saucedemo.com")

    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.get_by_role("button", name="Login").click()
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")

    cards = page.get_by_test_id("inventory-item")
    expect(cards).to_have_count(6)

    # Challenge 1: the trap. Substring match finds BOTH T-shirts
    t_shirts = cards.filter(has_text="T-Shirt")
    expect(t_shirts).to_have_count(2)
    print("has_text='T-Shirt' matched", t_shirts.count(), "cards")

    # Challenge 1: the fix. Exact match on the product name
    bolt = cards.filter(has=page.get_by_text("Sauce Labs Bolt T-Shirt", exact=True))
    expect(bolt).to_have_count(1)

    # Challenge 2, option 1: product-specific test id
    page.get_by_test_id("add-to-cart-sauce-labs-bike-light").click()
    expect(page.get_by_test_id("shopping-cart-badge")).to_have_text("1")

    # Challenge 2, option 2: data-driven, by product name
    for name in ["Sauce Labs Bolt T-Shirt", "Sauce Labs Backpack"]:
        add_to_cart(page, name)

    expect(page.get_by_test_id("shopping-cart-badge")).to_have_text("3")

    browser.close()