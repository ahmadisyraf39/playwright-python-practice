# Ex 0b: codegen recording (raw, not cleaned up)
# Command: playwright codegen demo.playwright.dev/todomvc
# Observations:
#  - codegen prefers get_by_role (role + accessible name)
#  - filter(has_text="test2") needed: two "Toggle Todo" checkboxes -> strict mode
#  - repeats the same locator 5x, adds useless click() before fill()
#  - Delete button only visible on hover -> may fail on replay

import re
from playwright.sync_api import Playwright, sync_playwright, expect

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://demo.playwright.dev/todomvc/#/")
    page.get_by_role("textbox", name="What needs to be done?").click()
    page.get_by_role("textbox", name="What needs to be done?").fill("test")
    page.get_by_role("textbox", name="What needs to be done?").press("Enter")
    page.get_by_role("textbox", name="What needs to be done?").fill("test2")
    page.get_by_role("textbox", name="What needs to be done?").press("Enter")
    page.get_by_role("listitem").filter(has_text="test2").get_by_label("Toggle Todo").check()
    page.get_by_role("link", name="Completed").click()
    page.get_by_role("link", name="Active").click()
    page.get_by_role("link", name="All").click()
    page.get_by_role("button", name="Delete").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
