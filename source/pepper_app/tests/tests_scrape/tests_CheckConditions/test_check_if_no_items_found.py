from pathlib import Path
import html5lib
import pytest
from bs4 import BeautifulSoup, Tag
from source.pepper_app.scrape import CheckConditions

@pytest.fixture
def soup_searched_item_not_found():
    """Preparing article for tests."""
    path_to_file = Path("source/pepper_app/tests/fixtures/to_test_scrape/soup_searched_item_not_found.html")
    with open(path_to_file, "r", encoding="utf-8") as file:
        soup = file.read()
    soup_searched_item_not_found = BeautifulSoup(soup, "html5lib")
    return soup_searched_item_not_found


@pytest.fixture
def soup_searched_item_found():
    """Preparing article for tests."""
    path_to_file = Path("source/pepper_app/tests/fixtures/to_test_scrape/soup_searched_item_found.html")
    with open(path_to_file, "r", encoding="utf-8") as file:
        soup = file.read()
    soup_searched_item_found = BeautifulSoup(soup, "html5lib")
    return soup_searched_item_found


def test_check_if_no_items_found_1(soup_searched_item_not_found):
    """Test if False is received when searched item is not found."""
    start_page = 1
    result = CheckConditions(soup_searched_item_not_found, start_page).check_if_no_items_found()
    assert result == False


def test_check_if_no_items_found_2(soup_searched_item_found):
    """Test if False is received when searched item is found."""
    start_page = 1
    result = CheckConditions(soup_searched_item_found, start_page).check_if_no_items_found()
    assert result == True



