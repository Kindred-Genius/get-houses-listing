import os

CHROME_DRIVER = "/Users/aba/home/utils/chromedriver/chromedriver"
if not "geckodriver" in os.environ["PATH"]: FIREFOX_DRIVER = "/Users/aba/home/utils/firefoxdriver/geckodriver"
else: FIREFOX_DRIVER = ""
HEADERS = {
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15",
    "Accept-Language":"en-GB,en;q=0.9",
}