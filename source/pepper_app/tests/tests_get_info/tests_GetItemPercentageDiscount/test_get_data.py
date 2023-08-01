from pathlib import Path
import html5lib
import pytest
from bs4 import BeautifulSoup, Tag

from pepper_app.get_info import GetItemPercentageDiscount

@pytest.fixture
def article():
    """Preparing article for tests."""
    path_to_file = Path("source/pepper_app/tests/fixtures/to_test_get_info/GetItemPercentageDiscount/saved_tag_article_with_percentage_discount.html")
    with open(path_to_file, "r", encoding="utf-8") as file:
        article_string = file.read()
    article = BeautifulSoup(article_string, "html5lib")
    return article

@pytest.fixture
def article_without_percentage_discount():
    """Preparing article for tests."""
    path_to_file = Path("source/pepper_app/tests/fixtures/to_test_get_info/GetItemPercentageDiscount/saved_tag_article_without_percentage_discount.html")
    with open(path_to_file, "r", encoding="utf-8") as file:
        article_string = file.read()
    article_without_percentage_discount = BeautifulSoup(article_string, "html5lib")
    return article_without_percentage_discount


def test_article_type(article):
    """Test correct data type of the article."""
    assert isinstance(article, Tag)


def test_get_data_returns_correct_percentage_discount_if_exists(article):
    """Test retriving correct percentage discount."""
    percentage_discount = GetItemPercentageDiscount(article).get_data()
    assert percentage_discount == -15.0
    assert isinstance(percentage_discount, float)



def test_get_data_returns_correct_percentage_discount_if_not_exists(article_without_percentage_discount):
    """Test retriving NA if correct percentage discount doesnt exists."""
    percentage_discounts = GetItemPercentageDiscount(article_without_percentage_discount).get_data()
    assert percentage_discounts == "NA"




