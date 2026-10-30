from playwright.sync_api import sync_playwright, expect

todos = ["Learn Playwright", "Learn Selenium", "Learn Automation"]

with sync_playwright() as p:

    for browser_type in [p.chromium, p.firefox, p.webkit]:

        browser = browser_type.launch(headless=False, slow_mo=500)
        page = browser.new_page()
        page.goto("https://demo.playwright.dev/todomvc")

        new_todo = page.get_by_placeholder("What needs to be done?")
        
        for todo in todos:
            new_todo.fill(todo)
            new_todo.press("Enter")

        expect(page.get_by_test_id("todo-title")).to_have_text(todos)

        page.screenshot(path=f"screenshots/todo-{browser_type.name}.png")

        browser.close()