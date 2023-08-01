from pathlib import Path
import html5lib
import pytest
from bs4 import BeautifulSoup, Tag
from pepper_app.get_info import GetItemAddedDate

@pytest.fixture
def article():
    """Preparing article for tests."""
    path_to_file = Path("source/pepper_app/tests/fixtures/to_test_get_info/GetItemAddedDate/saved_tag_article.html")
    with open(path_to_file, "r", encoding="utf-8") as file:
        article_string = file.read()
    article = BeautifulSoup(article_string, "html5lib")
    return article


def test_article_type(article):
    """Test correct data type of the article."""
    assert isinstance(article, Tag)


def test_get_raw_non_list_with_data(article):

    raw_string_list = GetItemAddedDate(article).get_raw_data()

    assert isinstance(raw_string_list, list)
    assert len(raw_string_list) > 0