from pathlib import Path
import html5lib
import pytest
from bs4 import BeautifulSoup, Tag

from source.pepper_app.get_info import GetItemRegularPrice

@pytest.fixture
def article():
    """Preparing article for tests."""
    path_to_file = Path("pepper_app/tests/fixtures/to_test_get_info/soup.html")
    with open(path_to_file, "r", encoding="utf-8") as file:
        soup = file.read()
    soup = BeautifulSoup(soup, "html5lib")
    articles = soup.find_all('article')
    article = articles[0] #Example article with regular price
    return article

@pytest.fixture
def article_without_regular_price():
    """Preparing article for tests."""
    path_to_file = Path("pepper_app/tests/fixtures/to_test_get_info/soup.html")
    with open(path_to_file, "r", encoding="utf-8") as file:
        soup = file.read()
    soup = BeautifulSoup(soup, "html5lib")
    articles = soup.find_all('article')
    article_without_regular_price = articles[8] #Example article without regular price
    return article_without_regular_price



def test_get_data_returns_correct_regular_price_if_exists(article):
    """Test retriving correct regular price."""
    regular_price = GetItemRegularPrice(article).get_data()
    assert regular_price == 9.99
    assert isinstance(regular_price, float)



def test_get_data_returns_correct_regular_price_if_not_exists(article_without_regular_price):
    """Test retriving NA if correct regular price doesnt exists."""
    regular_prices = GetItemRegularPrice(article_without_regular_price).get_data()
    assert regular_prices == "NA"




