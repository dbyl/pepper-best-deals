from pathlib import Path
import html5lib
import pytest
from bs4 import BeautifulSoup, Tag
from source.pepper_app.get_info import GetItemAddedDate

@pytest.fixture
def article():
    """Preparing article for tests."""
    path_to_file = Path("source/pepper_app/tests/fixtures/to_test_get_info/soup.html")
    with open(path_to_file, "r", encoding="utf-8") as file:
        soup = file.read()
    soup = BeautifulSoup(soup, "html5lib")
    articles = soup.find_all('article')
    article = articles[1] #Example article
    return article


def test_get_raw_data(article):
    """Test if non empty list is returned"""
    raw_string_list = GetItemAddedDate(article).clean_list()
    assert isinstance(raw_string_list, list)
    assert len(raw_string_list) > 0