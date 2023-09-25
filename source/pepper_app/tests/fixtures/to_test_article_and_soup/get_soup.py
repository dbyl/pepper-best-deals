from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time


def get_current_soup():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1400,1000)
    driver.get("https://www.pepper.pl/nowe")
    time.sleep(0.7)
    page = driver.page_source
    soup = BeautifulSoup(page, "html5lib")

    with open("pepper_app/tests/fixtures/to_test_article_and_soup/soup_to_check.html", 'w', encoding='utf-8') as file:
        file.write(str(soup))

    driver.quit()

