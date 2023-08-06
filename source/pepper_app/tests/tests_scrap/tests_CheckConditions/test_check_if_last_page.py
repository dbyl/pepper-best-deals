from pathlib import Path
import html5lib
import pytest
from bs4 import BeautifulSoup, Tag
from pepper_app.scrap import CheckConditions

@pytest.fixture
def soup():
    """Preparing article for tests."""
    path_to_file = Path("pepper_app/tests/fixtures/to_test_scrap/soup.html")
    with open(path_to_file, "r", encoding="utf-8") as file:
        soup = file.read()
    soup = BeautifulSoup(soup, "html5lib")
    return soup

@pytest.fixture
def soup_nowe_last_page():
    """Preparing article for tests."""
    path_to_file = Path("pepper_app/tests/fixtures/to_test_scrap/soup_nowe_last_page.html")
    with open(path_to_file, "r", encoding="utf-8") as file:
        soup = file.read()
    soup_nowe_last_page = BeautifulSoup(soup, "html5lib")
    return soup_nowe_last_page

@pytest.fixture
def soup_searched_item_last_page():
    """Preparing article for tests."""
    path_to_file = Path("pepper_app/tests/fixtures/to_test_scrap/soup_searched_item_last_page.html")
    with open(path_to_file, "r", encoding="utf-8") as file:
        soup = file.read()
    soup_searched_item_last_page = BeautifulSoup(soup, "html5lib")
    return soup_searched_item_last_page


def test_check_if_last_page_nowe_last_page(soup_nowe_last_page):
    """Test if False is received when last page in 'nowe' occured."""
    result = CheckConditions(soup_nowe_last_page).check_if_last_page_nowe()
    assert result == False


def test_check_if_last_page_searched_item_last_page(soup_searched_item_last_page):
    """Test if False is received when last page in 'search' occured."""
    result = CheckConditions(soup_searched_item_last_page).check_if_last_page_search()
    assert result == False


def test_check_if_last_page_nowe_non_last_page(soup):
    """Test if True is received when there are more pages in 'nowe' left."""
    result = CheckConditions(soup).check_if_last_page_nowe()
    assert result == True


def test_check_if_last_page_searched_item_non_last_page(soup):
    """Test if True is received when there are more pages in 'search' left."""
    result = CheckConditions(soup).check_if_last_page_search()
    assert result == True

