from playwright.sync_api import Playwright


class App:
    def __init__(self, playwright: Playwright):
        self.browser = playwright.chromium.launch(headless=False)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        self.page.goto("http://127.0.0.1:8000/login/?next=/")

    def login(self):
        self.page.fill("input[name=\"username\"]", "alice")
        self.page.fill("input[name=\"password\"]", "Qamania123")
        self.page.click("text=Login")

    def create_test(self):
        self.page.click("text=Create new test")
        self.page.fill("input[name=\"name\"]", "hello")
        self.page.fill("textarea[name=\"description\"]", "world")
        self.page.click("input:has-text(\"Create\")")

    def open_test(self):
        self.page.click("text=Test Cases")

    def check_test(self):
        assert self.page.query_selector('//td[text()="hello"]') is not None

    def delete_test(self):
        self. page.click("text=26 hello world alice Norun None PASS FAIL Details Delete >> :nth-match(button, 4)")

    def close(self):
        self.page.close()
        self.context.close()
        self.browser.close()
