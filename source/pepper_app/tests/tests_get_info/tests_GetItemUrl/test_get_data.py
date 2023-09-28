from pathlib import Path
import html5lib
import pytest
from bs4 import BeautifulSoup, Tag
from pepper_app.get_info import GetItemUrl

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


def test_get_data_returns_correct_url(article):
    """Test retriving correct article's url."""
    url = GetItemUrl(article).get_data()
    assert url == "https://www.pepper.pl/promocje/czerwona-papryka-kg-at-lidl-704489"


def test_get_data_returns_correct_type(article):
    """Test correct data type of the retrived url."""
    url = GetItemUrl(article).get_data()
    assert isinstance(url, str)
