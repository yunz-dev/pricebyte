from playwright.sync_api import sync_playwright

class ColesScraper:

    def __init__(self, headless = True):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=headless)
        self.page = self.browser.new_page()