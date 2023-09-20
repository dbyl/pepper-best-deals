from pathlib import Path
import html5lib
import pytest
import time
from bs4 import BeautifulSoup, Tag
from source.pepper_app.tests.fixtures.to_test_article_and_soup import get_article

get_article.get_current_article() #Collecting current soup.

@pytest.fixture
def current_article_soup():
    """Setting environment up."""
    time.sleep(0.7)
    path_to_file = Path("pepper_app/tests/fixtures/to_test_article_and_soup/article_to_check.html")
    with open(path_to_file, "r", encoding="utf-8") as file:
        current_article_soup = file.read()
    current_article_soup = BeautifulSoup(current_article_soup, "html5lib")
    return current_article_soup


def test_if_valid_class_with_added_date(current_article_soup):
    """Test if valid class with item added date exists."""
    bad, ok = 0, 0

    list_with_date = current_article_soup.find_all('div', {"class":"space--mv-3"})

    assert len(list_with_date) > 0
    assert isinstance(list_with_date, list)