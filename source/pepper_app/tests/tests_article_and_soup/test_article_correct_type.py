from pathlib import Path
import html5lib
import pytest
from bs4 import BeautifulSoup, Tag

@pytest.fixture
def article():
    """Preparing article for tests."""
    path_to_file = Path("source/pepper_app/tests/fixtures/to_test_article_and_soup/soup.html")
    with open(path_to_file, "r", encoding="utf-8") as file:
        soup = file.read()
    soup = BeautifulSoup(soup, "html5lib")
    articles = soup.find_all('article')
    article = articles[0] #Example article
    return article


def test_article_type(article):
    """Test correct data type of the article."""
    assert isinstance(article, Tag)







