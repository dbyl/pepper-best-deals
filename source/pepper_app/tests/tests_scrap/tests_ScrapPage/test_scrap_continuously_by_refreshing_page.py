from pathlib import Path
import html5lib
from pytest_mock import mocker
import pytest
from bs4 import BeautifulSoup, Tag
from pepper_app.scrap import ScrapPage, CheckConditions


@pytest.fixture
def soup():
    """Preparing article for tests."""
    path_to_file = Path("pepper_app/tests/fixtures/to_test_scrap/soup.html")
    with open(path_to_file, "r", encoding="utf-8") as file:
        soup = file.read()
    soup = BeautifulSoup(soup, "html5lib")
    return soup

def test_scrap_continuously_by_refreshing_page_1(mocker, soup):
    """Test scrap continuously by refreshing page if correct list filled with articles is returned."""
    category_type = "nowe"
    articles_to_retrieve = 50

    scrap_page_mock = mocker.patch("pepper_app.scrap.ScrapPage.scrap_page")

    scrap_page_mock.return_value = soup

    retrived_articles = ScrapPage(category_type=category_type, articles_to_retrieve=articles_to_retrieve).scrap_continuously_by_refreshing_page()

    assert isinstance(retrived_articles, list)
    assert len(retrived_articles) > 0

