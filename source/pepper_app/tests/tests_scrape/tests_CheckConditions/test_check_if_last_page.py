from pathlib import Path
import html5lib
import pytest
from bs4 import BeautifulSoup, Tag
from source.pepper_app.scrape import CheckConditions

@pytest.fixture
def soup():
    """Preparing article for tests."""
    path_to_file = Path("source/pepper_app/tests/fixtures/to_test_scrape/soup.html")
    with open(path_to_file, "r", encoding="utf-8") as file:
        soup = file.read()
    soup = BeautifulSoup(soup, "html5lib")
    return soup


@pytest.fixture
def soup_searched_item_last_page():
    """Preparing article for tests."""
    path_to_file = Path("source/pepper_app/tests/fixtures/to_test_scrape/soup_searched_item_last_page.html")
    with open(path_to_file, "r", encoding="utf-8") as file:
        soup = file.read()
    soup_searched_item_last_page = BeautifulSoup(soup, "html5lib")
    return soup_searched_item_last_page


def test_check_if_last_page_1(soup):
    """Test if False is received when last page in 'nowe' occured."""
    start_page = 335
    result = CheckConditions(soup, start_page).check_if_last_page_nowe()
    assert result == False


def test_check_if_last_page_2(soup_searched_item_last_page):
    """Test if False is received when last page in 'search' occured."""
    start_page = 1
    result = CheckConditions(soup_searched_item_last_page, start_page).check_if_last_page_search()
    assert result == False


def test_check_if_last_page_nowe_non_last_page(soup):
    """Test if True is received when there are more pages in 'nowe' left."""
    start_page = 1
    result = CheckConditions(soup, start_page).check_if_last_page_nowe()
    assert result == True


def test_check_if_last_page_searched_item_non_last_page(soup):
    """Test if True is received when there are more pages in 'search' left."""
    start_page = 1
    result = CheckConditions(soup, start_page).check_if_last_page_search()
    assert result == True

