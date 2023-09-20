from pathlib import Path
import html5lib
from pytest_mock import mocker
import pytest
from unittest.mock import patch
from bs4 import BeautifulSoup, Tag
from source.pepper_app.scrap import ScrapPage, CheckConditions


@pytest.fixture
def soup():
    """Preparing article for tests."""
    path_to_file = Path("pepper_app/tests/fixtures/to_test_scrap/soup.html")
    with open(path_to_file, "r", encoding="utf-8") as file:
        soup = file.read()
    soup = BeautifulSoup(soup, "html5lib")
    return soup


def test_infinite_scroll_handling_1(mocker, soup):
    """Test infinite scroll handling if the page in 'nowe' is not last."""
    scrap_continuously = False
    category_type = "nowe"
    articles_to_retrieve = 50

    select_url_mock = mocker.patch("source.pepper_app.scrap.ScrapPage.select_url")
    scrap_page_mock = mocker.patch("source.pepper_app.scrap.ScrapPage.scrap_page")
    check_if_last_page_nowe_mock = mocker.patch("source.pepper_app.scrap.CheckConditions.check_if_last_page_nowe")
    check_if_last_page_search_mock = mocker.patch("source.pepper_app.scrap.CheckConditions.check_if_last_page_search")
    check_if_no_items_found_mock = mocker.patch("source.pepper_app.scrap.CheckConditions.check_if_no_items_found")

    select_url_mock.return_value = "https://www.pepper.pl/nowe?page=1"
    scrap_page_mock.return_value = soup
    check_if_last_page_nowe_mock.return_value = True
    check_if_last_page_search_mock.return_value = True
    check_if_no_items_found_mock.return_value = True

    retrived_articles = ScrapPage(category_type=category_type, articles_to_retrieve=articles_to_retrieve).infinite_scroll_handling()

    assert isinstance(retrived_articles, list)
    assert len(retrived_articles) > 0


def test_infinite_scroll_handling_2(mocker, soup):
    """Test infinite scroll handling if the page in 'nowe' is not last with only one article to retrieve."""
    scrap_continuously = False
    category_type = "nowe"
    articles_to_retrieve = 1

    select_url_mock = mocker.patch("source.pepper_app.scrap.ScrapPage.select_url")
    scrap_page_mock = mocker.patch("source.pepper_app.scrap.ScrapPage.scrap_page")
    check_if_last_page_nowe_mock = mocker.patch("source.pepper_app.scrap.CheckConditions.check_if_last_page_nowe")
    check_if_last_page_search_mock = mocker.patch("source.pepper_app.scrap.CheckConditions.check_if_last_page_search")
    check_if_no_items_found_mock = mocker.patch("source.pepper_app.scrap.CheckConditions.check_if_no_items_found")

    select_url_mock.return_value = "https://www.pepper.pl/nowe?page=1"
    scrap_page_mock.return_value = soup
    check_if_last_page_nowe_mock.return_value = True
    check_if_last_page_search_mock.return_value = True
    check_if_no_items_found_mock.return_value = True

    retrived_articles = ScrapPage(category_type=category_type, articles_to_retrieve=articles_to_retrieve).infinite_scroll_handling()

    assert isinstance(retrived_articles, list)
    assert len(retrived_articles) > 0


def test_infinite_scroll_handling_3(mocker, soup):
    """Test infinite scroll handling if the page in 'search' is last."""
    scrap_continuously = False
    category_type = "search"
    articles_to_retrieve = 50

    select_url_mock = mocker.patch("source.pepper_app.scrap.ScrapPage.select_url")
    scrap_page_mock = mocker.patch("source.pepper_app.scrap.ScrapPage.scrap_page")
    check_if_last_page_nowe_mock = mocker.patch("source.pepper_app.scrap.CheckConditions.check_if_last_page_nowe")
    check_if_last_page_search_mock = mocker.patch("source.pepper_app.scrap.CheckConditions.check_if_last_page_search")

    select_url_mock.return_value = "https://www.pepper.pl/search?q=s21&page=1"
    scrap_page_mock.return_value = soup
    check_if_last_page_nowe_mock.return_value = True
    check_if_last_page_search_mock.return_value = False

    retrived_articles = ScrapPage(category_type=category_type, articles_to_retrieve=articles_to_retrieve).infinite_scroll_handling()

    assert isinstance(retrived_articles, list)
    assert len(retrived_articles) == 0


def test_infinite_scroll_handling_4(mocker, soup):
    """Test infinite scroll handling if the searched item is not found."""
    scrap_continuously = False
    category_type = "search"
    articles_to_retrieve = 50

    select_url_mock = mocker.patch("source.pepper_app.scrap.ScrapPage.select_url")
    scrap_page_mock = mocker.patch("source.pepper_app.scrap.ScrapPage.scrap_page")
    check_if_last_page_nowe_mock = mocker.patch("source.pepper_app.scrap.CheckConditions.check_if_last_page_nowe")
    check_if_last_page_search_mock = mocker.patch("source.pepper_app.scrap.CheckConditions.check_if_last_page_search")
    check_if_no_items_found_mock = mocker.patch("source.pepper_app.scrap.CheckConditions.check_if_no_items_found")

    select_url_mock.return_value = "https://www.pepper.pl/search?q=asdasdasd&page=1"
    scrap_page_mock.return_value = soup
    check_if_last_page_nowe_mock.return_value = True
    check_if_last_page_search_mock.return_value = True
    check_if_no_items_found_mock.return_value = False

    retrived_articles = ScrapPage(category_type=category_type, articles_to_retrieve=articles_to_retrieve).infinite_scroll_handling()

    assert isinstance(retrived_articles, list)
    assert len(retrived_articles) == 0

