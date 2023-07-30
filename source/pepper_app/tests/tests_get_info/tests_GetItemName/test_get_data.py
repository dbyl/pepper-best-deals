from pathlib import Path
import html5lib
import pytest
from bs4 import BeautifulSoup, Tag
from pepper_app.get_info import GetItemName

@pytest.fixture
def article():
    """Preparing article for tests."""
    path_to_file = Path("source/pepper_app/tests/fixtures/to_test_get_info/GetItemName/saved_tag_article.html")
    with open(path_to_file, "r", encoding="utf-8") as file:
        article_string = file.read()
    article = BeautifulSoup(article_string, "html5lib")
    return article


def test_article_type(article):
    """Test correct data type of the article."""
    assert isinstance(article, Tag)


def test_get_data_returns_correct_name(article):
    """Test retriving correct article's name."""
    name = GetItemName(article).get_data()
    assert name == "PARKSIDE Wiertarkowkrętarka akumulatorowa 20 V PABS 20-Li E6 (bez aku i ładowarki)"


def test_get_data_returns_correct_type(article):
    """Test correct data type of the retrived name."""
    name = GetItemName(article).get_data()
    assert isinstance(name, str)
