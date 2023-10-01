from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

#selenium_url = "http://172.21.0.2:4444"


def get_current_article():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    #driver = webdriver.Remote(command_executor=selenium_url, options=options)
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1400,1000)
    driver.get("https://www.pepper.pl/nowe")
    time.sleep(0.7)
    page = driver.page_source
    soup = BeautifulSoup(page, "html5lib")

    all_articles = soup.find_all('article')
    item_url = all_articles[0].find_all('a', {"class":"cept-tt thread-link linkPlain thread-title--list js-thread-title"})[0]['href']
    driver.get(item_url)
    time.sleep(0.7)
    page_with_article = driver.page_source
    soup_with_article = BeautifulSoup(page_with_article, "html5lib")

    with open("pepper_app/tests/fixtures/to_test_article_and_soup/article_to_check.html", 'w', encoding='utf-8') as file:
        file.write(str(soup_with_article))

    driver.quit()

