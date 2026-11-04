import re
from playwright.sync_api import Page, expect

BACKPACK = "Sauce Labs Backpack"
BIKE_LIGHT = "Sauce Labs Bike Light"

def login(page: Page) -> None:
    # go to saucedemo, log in as standard_user, check you reached the inventory page
    page.goto("https://www.saucedemo.com/")
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.get_by_role("button", name="Login").click()
    expect(page).to_have_url(re.compile(r".*/inventory\.html$"))

def product_card(page: Page, product_name: str):
    """The inventory card whose product name matches exactly."""
    cards = page.get_by_test_id("inventory-item")
    return cards.filter(has=page.get_by_text(product_name, exact=True))

def add_to_cart(page: Page, product_name: str) -> None:
    # find the product card by its exact name, click its "Add to cart" button
    # (you wrote this in 1e)
    card = product_card(page, product_name)
    card.get_by_role("button", name="Add to cart").click()
    expect(card.get_by_role("button", name="Remove")).to_be_visible()

def remove_from_cart(page: Page, product_name: str) -> None:
    card = product_card(page, product_name)
    card.get_by_role("button", name="Remove").click()
    expect(card.get_by_role("button", name="Add to cart")).to_be_visible()
    
def test_badge_counts_added_items(page: Page):
    # log in, add 2 different products
    # assert the badge shows "2"
    login(page)
    add_to_cart(page, BACKPACK)
    add_to_cart(page, BIKE_LIGHT)

    expect(page.get_by_test_id("shopping-cart-badge")).to_have_text("2")


def test_badge_decreases_after_remove(page: Page):
    # log in, add 2 products, remove 1 of them
    # assert the badge shows "1"
    login(page)
    add_to_cart(page, BACKPACK)
    add_to_cart(page, BIKE_LIGHT)
    remove_from_cart(page, BACKPACK)

    expect(page.get_by_test_id("shopping-cart-badge")).to_have_text("1")


def test_badge_hidden_when_cart_empty(page: Page):
    # log in, assert there's no badge at the start
    # add 1 product, assert the badge shows "1"
    # remove it, assert the badge is gone again
    login(page)
    badge = page.get_by_test_id("shopping-cart-badge")

    expect(badge).to_have_count(0)          # no badge at the start

    add_to_cart(page, BACKPACK)
    expect(badge).to_have_text("1")         # badge appears

    remove_from_cart(page, BACKPACK)
    expect(badge).to_have_count(0)          # badge gone again