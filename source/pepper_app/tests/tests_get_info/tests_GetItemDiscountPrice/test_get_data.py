from pathlib import Path
import html5lib
import pytest
from bs4 import BeautifulSoup, Tag

from source.pepper_app.get_info import GetItemDiscountPrice

@pytest.fixture
def article():
    """Preparing article for tests."""
    path_to_file = Path("source/pepper_app/tests/fixtures/to_test_get_info/soup.html")
    with open(path_to_file, "r", encoding="utf-8") as file:
        soup = file.read()
    soup = BeautifulSoup(soup, "html5lib")
    articles = soup.find_all('article')
    article = articles[0] #Example article with discount price
    return article

@pytest.fixture
def article_without_discount_price():
    """Preparing article for tests."""
    path_to_file = Path("source/pepper_app/tests/fixtures/to_test_get_info/soup.html")
    with open(path_to_file, "r", encoding="utf-8") as file:
        soup = file.read()
    soup = BeautifulSoup(soup, "html5lib")
    articles = soup.find_all('article')
    article = articles[22] #Example article without discount price
    return article


def test_get_data_1(article):
    """Test retriving correct discount price."""
    discount_price = GetItemDiscountPrice(article).get_data()
    assert discount_price == 211.72
    assert isinstance(discount_price, float)


def test_get_data_2(article_without_discount_price):
    """Test retriving NA if correct discount price doesnt exists."""
    discount_prices = GetItemDiscountPrice(article_without_discount_price).get_data()
    assert discount_prices == "NA"




