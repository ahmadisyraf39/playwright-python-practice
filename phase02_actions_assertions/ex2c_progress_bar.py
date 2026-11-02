import re
from playwright.sync_api import sync_playwright, expect

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("http://uitestingplayground.com/progressbar")

    # 1. Locate the Start button, the Stop button, and the progress bar
    start = page.get_by_role("button", name="Start")
    stop = page.get_by_role("button", name="Stop")
    bar = page.get_by_role("progressbar")

    # 2. Click Start
    start.click()

    # 3. Wait until the progress bar's value is 75 or more
    #    (how long does the bar take to reach 75? give enough timeout)
    expect(bar).to_have_attribute(
        "aria-valuenow",
        re.compile(r"^(7[5-9]|[89]\d|100)$"),
        timeout=30_000,
    )

    # 4. Click Stop immediately
    stop.click()

    # 5. Read the final value as a number, assert it's >= 75, print it
    bar_final_value = int (bar.get_attribute("aria-valuenow"))
    assert bar_final_value >= 75, f"stopped too early at {bar_final_value}"
    print(f"Stopped at: {bar_final_value}%")

    # 6. Print the result text the page shows below the bar
    print(page.locator("#result").inner_text())

    browser.close()