from pathlib import Path
import html5lib
import pytest
from bs4 import BeautifulSoup, Tag

from source.pepper_app.get_info import GetItemPercentageDiscount

@pytest.fixture
def article():
    """Preparing article for tests."""
    path_to_file = Path("source/pepper_app/tests/fixtures/to_test_get_info/soup.html")
    with open(path_to_file, "r", encoding="utf-8") as file:
        soup = file.read()
    soup = BeautifulSoup(soup, "html5lib")
    articles = soup.find_all('article')
    article = articles[0] #Example article with regular price
    return article

@pytest.fixture
def article_without_percentage_discount():
    """Preparing article for tests."""
    path_to_file = Path("source/pepper_app/tests/fixtures/to_test_get_info/soup.html")
    with open(path_to_file, "r", encoding="utf-8") as file:
        soup = file.read()
    soup = BeautifulSoup(soup, "html5lib")
    articles = soup.find_all('article')
    article_without_percentage_discount = articles[15] #Example article without percentage discount
    return article_without_percentage_discount



def test_get_data_returns_correct_percentage_discount_if_exists(article):
    """Test retriving correct percentage discount."""
    percentage_discount = GetItemPercentageDiscount(article).get_data()
    assert percentage_discount == -30.0
    assert isinstance(percentage_discount, float)



def test_get_data_returns_correct_percentage_discount_if_not_exists(article_without_percentage_discount):
    """Test retriving NA if correct percentage discount doesnt exists."""
    percentage_discounts = GetItemPercentageDiscount(article_without_percentage_discount).get_data()
    assert percentage_discounts == "NA"




