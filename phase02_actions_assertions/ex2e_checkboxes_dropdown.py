from playwright.sync_api import sync_playwright, expect

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=500)
    page = browser.new_page()

    # ---------- Checkboxes ----------
    page.goto("https://the-internet.herokuapp.com/checkboxes")

    # 1. Locate both checkboxes (no labels: which get_by_role? how to pick each?)
    checkboxes = page.get_by_role("checkbox")
    checkbox1 = checkboxes.nth(0)
    checkbox2 = checkboxes.nth(1)

    # 2. Assert the STARTING state (inspect first: which one starts ticked?)
    expect(checkbox1).not_to_be_checked
    expect(checkbox2).to_be_checked

    # 3. Tick checkbox 1, untick checkbox 2
    checkbox1.check()
    checkbox2.uncheck()

    # 4. Assert the new states
    expect(checkbox1).to_be_checked
    expect(checkbox2).not_to_be_checked

    # ---------- Dropdown ----------
    page.goto("https://the-internet.herokuapp.com/dropdown")

    # 5. Locate the dropdown
    dropdown = page.locator("#dropdown")

    # 6. Select "Option 2" by its visible text
    dropdown.select_option(label="Option 2")

    # 7. Assert the selected VALUE (inspect the <option> elements)
    expect(dropdown).to_have_value("2")

    # 8. Select Option 1 by value, assert again
    dropdown.select_option(label="Option 1")
    expect(dropdown).to_have_value("1")

    browser.close()