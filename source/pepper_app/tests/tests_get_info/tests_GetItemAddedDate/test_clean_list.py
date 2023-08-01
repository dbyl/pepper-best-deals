from pathlib import Path
import html5lib
import pytest
from bs4 import BeautifulSoup, Tag
from pepper_app.get_info import GetItemAddedDate

@pytest.fixture
def article():
    """Preparing article for tests."""
    path_to_file = Path("source/pepper_app/tests/fixtures/to_test_get_info/GetItemAddedDate/clean_list_items_to_clean.html")
    with open(path_to_file, "r", encoding="utf-8") as file:
        article_string = file.read()
    article = BeautifulSoup(article_string, "html5lib")
    return article


def test_article_type(article):
    """Test correct data type of the article."""
    assert isinstance(article, Tag)


def test_clean_list(article):
    """Test if returns list without forbidden strings"""
    filtered_list = GetItemAddedDate(article).clean_list()

    assert filtered_list == ["17 min"]
