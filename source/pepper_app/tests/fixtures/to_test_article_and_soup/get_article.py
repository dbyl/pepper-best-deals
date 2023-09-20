from selenium import webdriver
from bs4 import BeautifulSoup
import time

def get_current_article():
    driver = webdriver.Chrome()
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

