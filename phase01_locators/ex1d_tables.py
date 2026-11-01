from playwright.sync_api import sync_playwright, expect, Locator


def find_highest_due(rows: Locator, email_selector: str, due_selector: str) -> tuple[str, float]:
    """Return (email, due) for the row with the highest Due amount."""
    highest_due = 0.0
    highest_email = None

    for row in rows.all():
        email = row.locator(email_selector).inner_text()
        due_text = row.locator(due_selector).inner_text()     
        due = float(due_text.replace("$", ""))

        if due > highest_due:
            highest_due = due
            highest_email = email

    assert highest_email is not None, "no rows were read"
    return highest_email, highest_due


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=500)
    page = browser.new_page()
    page.goto("https://the-internet.herokuapp.com/tables")

    # Table 1: no classes on cells, so select by column position
    rows_table1 = page.locator("#table1 tbody tr")
    expect(rows_table1).to_have_count(4)
    email1, due1 = find_highest_due(rows_table1, "td:nth-child(3)", "td:nth-child(4)")
    print(f"Table 1 highest due: {email1} (${due1:.2f})")

    # Table 2 (bonus): cells have classes describing their column
    rows_table2 = page.locator("#table2 tbody tr")
    expect(rows_table2).to_have_count(4)
    email2, due2 = find_highest_due(rows_table2, "td.email", "td.dues")
    print(f"Table 2 highest due: {email2} (${due2:.2f})")

    # Both tables hold the same data, so the answers must match
    assert (email1, due1) == (email2, due2), f"{email1} != {email2}"

    browser.close()