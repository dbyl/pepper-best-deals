from pathlib import Path
import html5lib
import pytest
from bs4 import BeautifulSoup, Tag
from pepper_app.get_info import GetItemId

@pytest.fixture
def article():
    """Preparing article for tests."""
    path_to_file = Path("source/pepper_app/tests/fixtures/to_test_get_info/GetItemId/saved_tag_article.html")
    with open(path_to_file, "r", encoding="utf-8") as file:
        article_string = file.read()
    article = BeautifulSoup(article_string, "html5lib")
    return article


def test_article_type(article):
    """Test correct data type of the article."""
    assert isinstance(article, Tag)


def test_get_data_returns_correct_id_string(article):
    """Test retriving correct id string."""
    item_id = GetItemId(article).get_data()
    assert item_id == 703221
    assert isinstance(item_id, int)




