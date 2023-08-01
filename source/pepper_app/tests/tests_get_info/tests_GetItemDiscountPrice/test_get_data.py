from pathlib import Path
import html5lib
import pytest
from bs4 import BeautifulSoup, Tag

from pepper_app.get_info import GetItemDiscountPrice

@pytest.fixture
def article():
    """Preparing article for tests."""
    path_to_file = Path("source/pepper_app/tests/fixtures/to_test_get_info/GetItemDiscountPrice/saved_tag_article_with_discount_price.html")
    with open(path_to_file, "r", encoding="utf-8") as file:
        article_string = file.read()
    article = BeautifulSoup(article_string, "html5lib")
    return article

@pytest.fixture
def article_without_discount_price():
    """Preparing article for tests."""
    path_to_file = Path("source/pepper_app/tests/fixtures/to_test_get_info/GetItemDiscountPrice/saved_tag_article_without_discount_price.html")
    with open(path_to_file, "r", encoding="utf-8") as file:
        article_string = file.read()
    article_without_discount_price = BeautifulSoup(article_string, "html5lib")
    return article_without_discount_price


def test_article_type(article):
    """Test correct data type of the article."""
    assert isinstance(article, Tag)


def test_get_data_returns_correct_discount_price_if_exists(article):
    """Test retriving correct discount price."""
    discount_price = GetItemDiscountPrice(article).get_data()
    assert discount_price == 91.63
    assert isinstance(discount_price, float)



def test_get_data_returns_correct_discount_price_if_not_exists(article_without_discount_price):
    """Test retriving NA if correct discount price doesnt exists."""
    discount_prices = GetItemDiscountPrice(article_without_discount_price).get_data()
    assert discount_prices == "NA"




