from pathlib import Path
import html5lib
import pytest
from bs4 import BeautifulSoup, Tag

from pepper_app.get_info import GetItemRegularPrice

@pytest.fixture
def article():
    """Preparing article for tests."""
    path_to_file = Path("source/pepper_app/tests/fixtures/to_test_get_info/GetItemRegularPrice/saved_tag_article_with_regular_price.html")
    with open(path_to_file, "r", encoding="utf-8") as file:
        article_string = file.read()
    article = BeautifulSoup(article_string, "html5lib")
    return article

@pytest.fixture
def article_without_regular_price():
    """Preparing article for tests."""
    path_to_file = Path("source/pepper_app/tests/fixtures/to_test_get_info/GetItemRegularPrice/saved_tag_article_without_regular_price.html")
    with open(path_to_file, "r", encoding="utf-8") as file:
        article_string = file.read()
    article_without_regular_price = BeautifulSoup(article_string, "html5lib")
    return article_without_regular_price


def test_article_type(article):
    """Test correct data type of the article."""
    assert isinstance(article, Tag)


def test_get_data_returns_correct_regular_price_if_exists(article):
    """Test retriving correct regular price."""
    regular_price = GetItemRegularPrice(article).get_data()
    assert regular_price == 699
    assert isinstance(regular_price, float)



def test_get_data_returns_correct_regular_price_if_not_exists(article_without_regular_price):
    """Test retriving NA if correct regular price doesnt exists."""
    regular_prices = GetItemRegularPrice(article_without_regular_price).get_data()
    assert regular_prices == "NA"




