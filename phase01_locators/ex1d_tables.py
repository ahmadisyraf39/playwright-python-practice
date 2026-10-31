from playwright.sync_api import sync_playwright, expect

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=500)
    page = browser.new_page()
    page.goto("https://the-internet.herokuapp.com/tables")

    # 1. Locate all data rows of Table 1
    rows = page.locator("#table1 tbody tr")

    # 2. Check there are 4 rows (to_have_count)
    expect(rows).to_have_count(4)

    # 3. Loop over the rows. For each row:
    #    - read the email cell text
    #    - read the due cell text, e.g. "$50.00"
    #    - convert due to a number
    #    - keep track of the highest due and its email

    highest_due = 0
    highest_email = None

    for row in rows.all():
        cells = row.locator("td")

        email = cells.nth(2).inner_text()            # text of the email cell
        due_text = cells.nth(3).inner_text()         # text of the due cell, e.g. "$50.00"
        due = float(due_text.replace("$", ""))       # convert due_text to a float

        if due > highest_due:
            highest_due = due
            highest_email = email

    assert highest_email is not None, "no rows were read"

    # 4. Print the result
    print(f"Highest due: {highest_email} (${highest_due:.2f})")

    browser.close()