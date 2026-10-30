from playwright.sync_api import sync_playwright, expect

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=500)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://uitestingplayground.com/dynamicid")

     # 1. Create a locator for the button WITHOUT using its id
    element = page.get_by_role("button", name="Button with Dynamic ID")

    # 2. Check the button is visible, then click it
    expect(element).to_be_visible()
    element.click()

    # 3. Prove the id really changes:
    #    - read the button's id and save it
    btn_original_id = element.get_attribute("id")

    #    - reload the page
    page.reload()

    #    - read the id again
    btn_new_id = element.get_attribute("id")

    #    - print both, and assert they are different
    print(btn_original_id)
    print(btn_new_id)

    assert btn_original_id and btn_new_id, "button has no id"
    assert btn_new_id != btn_original_id

    browser.close()