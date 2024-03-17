from pathlib import Path
import html5lib
from pytest_mock import mocker
import pytest
from unittest.mock import patch
from bs4 import BeautifulSoup, Tag
from source.pepper_app.scrape import ScrapePage


@pytest.fixture
def soup():
    """Preparing article for tests."""
    path_to_file = Path("source/pepper_app/tests/fixtures/to_test_scrape/soup.html")
    with open(path_to_file, "r", encoding="utf-8") as file:
        soup = file.read()
    soup = BeautifulSoup(soup, "html5lib")
    return soup


@pytest.fixture
def soup_searched_item_not_found():
    """Preparing article for tests."""
    path_to_file = Path("source/pepper_app/tests/fixtures/to_test_scrape/soup_searched_item_not_found.html")
    with open(path_to_file, "r", encoding="utf-8") as file:
        soup = file.read()
    soup_searched_item_not_found = BeautifulSoup(soup, "html5lib")
    return soup_searched_item_not_found


@pytest.fixture
def soup_searched_item_last_page():
    """Preparing article for tests."""
    path_to_file = Path("source/pepper_app/tests/fixtures/to_test_scrape/soup_searched_item_last_page.html")
    with open(path_to_file, "r", encoding="utf-8") as file:
        soup = file.read()
    soup_searched_item_last_page = BeautifulSoup(soup, "html5lib")
    return soup_searched_item_last_page


def test_infinite_scroll_handling_1(mocker, soup):
    """Test infinite scroll handling if the page in 'nowe' is not last."""
    category_type = "nowe"
    articles_to_retrieve = 50

    select_url_mock = mocker.patch("source.pepper_app.scrape.ScrapePage.select_url")
    scrape_page_mock = mocker.patch("source.pepper_app.scrape.ScrapePage.scrape_page")
    check_if_last_page_nowe_mock = mocker.patch("source.pepper_app.scrape.CheckConditions.check_if_last_page_nowe")
    check_if_last_page_search_mock = mocker.patch("source.pepper_app.scrape.CheckConditions.check_if_last_page_search")
    check_if_no_items_found_mock = mocker.patch("source.pepper_app.scrape.CheckConditions.check_if_no_items_found")

    select_url_mock.return_value = "https://www.pepper.pl/nowe?page=1"
    scrape_page_mock.return_value = soup
    check_if_last_page_nowe_mock.return_value = True
    check_if_last_page_search_mock.return_value = True
    check_if_no_items_found_mock.return_value = True

    all_items = ScrapePage(category_type=category_type, articles_to_retrieve=articles_to_retrieve).infinite_scroll_handling()

    assert isinstance(all_items, list)
    assert len(all_items) > 0


def test_infinite_scroll_handling_2(mocker, soup):
    """Test infinite scroll handling if the page in 'nowe' is not last with only one article to retrieve."""
    category_type = "nowe"
    articles_to_retrieve = 1

    select_url_mock = mocker.patch("source.pepper_app.scrape.ScrapePage.select_url")
    scrape_page_mock = mocker.patch("source.pepper_app.scrape.ScrapePage.scrape_page")
    check_if_last_page_nowe_mock = mocker.patch("source.pepper_app.scrape.CheckConditions.check_if_last_page_nowe")
    check_if_last_page_search_mock = mocker.patch("source.pepper_app.scrape.CheckConditions.check_if_last_page_search")
    check_if_no_items_found_mock = mocker.patch("source.pepper_app.scrape.CheckConditions.check_if_no_items_found")

    select_url_mock.return_value = "https://www.pepper.pl/nowe?page=1"
    scrape_page_mock.return_value = soup
    check_if_last_page_nowe_mock.return_value = True
    check_if_last_page_search_mock.return_value = True
    check_if_no_items_found_mock.return_value = True

    all_items = ScrapePage(category_type=category_type, articles_to_retrieve=articles_to_retrieve).infinite_scroll_handling()

    assert isinstance(all_items, list)
    assert len(all_items) > 0


def test_infinite_scroll_handling_3(mocker, soup_searched_item_last_page):
    """Test infinite scroll handling if the page in 'search' is last."""
    category_type = "search"
    articles_to_retrieve = 50

    select_url_mock = mocker.patch("source.pepper_app.scrape.ScrapePage.select_url")
    scrape_page_mock = mocker.patch("source.pepper_app.scrape.ScrapePage.scrape_page")
    check_if_last_page_nowe_mock = mocker.patch("source.pepper_app.scrape.CheckConditions.check_if_last_page_nowe")
    check_if_last_page_search_mock = mocker.patch("source.pepper_app.scrape.CheckConditions.check_if_last_page_search")

    select_url_mock.return_value = "https://www.pepper.pl/search?q=s21&page=19"
    scrape_page_mock.return_value = soup_searched_item_last_page
    check_if_last_page_nowe_mock.return_value = False
    check_if_last_page_search_mock.return_value = True

    all_items = ScrapePage(category_type=category_type, articles_to_retrieve=articles_to_retrieve).infinite_scroll_handling()

    assert isinstance(all_items, list)
    assert len(all_items) == 4


def test_infinite_scroll_handling_4(mocker, soup_searched_item_not_found):
    """Test infinite scroll handling if the searched item is not found."""
    category_type = "search"
    articles_to_retrieve = 50

    select_url_mock = mocker.patch("source.pepper_app.scrape.ScrapePage.select_url")
    scrape_page_mock = mocker.patch("source.pepper_app.scrape.ScrapePage.scrape_page")
    check_if_last_page_nowe_mock = mocker.patch("source.pepper_app.scrape.CheckConditions.check_if_last_page_nowe")
    check_if_last_page_search_mock = mocker.patch("source.pepper_app.scrape.CheckConditions.check_if_last_page_search")
    check_if_no_items_found_mock = mocker.patch("source.pepper_app.scrape.CheckConditions.check_if_no_items_found")

    select_url_mock.return_value = "https://www.pepper.pl/search?q=asdasdasd&page=1"
    scrape_page_mock.return_value = soup_searched_item_not_found
    check_if_last_page_nowe_mock.return_value = True
    check_if_last_page_search_mock.return_value = True
    check_if_no_items_found_mock.return_value = False

    all_items = ScrapePage(category_type=category_type, articles_to_retrieve=articles_to_retrieve).infinite_scroll_handling()

    print(all_items)
    assert isinstance(all_items, list)
    assert len(all_items) == 0

