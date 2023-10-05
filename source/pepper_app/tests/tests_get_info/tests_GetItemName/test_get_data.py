from pathlib import Path
import html5lib
import pytest
from bs4 import BeautifulSoup, Tag
from source.pepper_app.get_info import GetItemName

@pytest.fixture
def article():
    """Preparing article for tests."""
    path_to_file = Path("source/pepper_app/tests/fixtures/to_test_get_info/soup.html")
    with open(path_to_file, "r", encoding="utf-8") as file:
        soup = file.read()
    soup = BeautifulSoup(soup, "html5lib")
    articles = soup.find_all('article')
    article = articles[0] #Example article
    return article


def test_get_data_returns_correct_name(article):
    """Test retriving correct article's name."""
    name = GetItemName(article).get_data()
    assert name == "Czerwona papryka kg @Lidl"


def test_get_data_returns_correct_type(article):
    """Test correct data type of the retrived name."""
    name = GetItemName(article).get_data()
    assert isinstance(name, str)
