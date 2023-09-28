from pathlib import Path
import html5lib
import pytest
from bs4 import BeautifulSoup, Tag
from source.pepper_app.scrap import ScrapPage
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from requests.exceptions import ConnectionError, MissingSchema, HTTPError, ReadTimeout



@pytest.fixture
def mock_driver(mocker):
    mock = mocker.MagicMock()
    return mock

@pytest.fixture
def mock_driver_connection_error(mocker):
    mock = mocker.MagicMock()
    mock.get.side_effect = ConnectionError()
    return mock

@pytest.fixture
def mock_driver_missing_schema(mocker):
    mock = mocker.MagicMock()
    mock.get.side_effect = MissingSchema()
    return mock

@pytest.fixture
def mock_driver_http_error(mocker):
    mock = mocker.MagicMock()
    mock.get.side_effect = HTTPError()
    return mock

@pytest.fixture
def mock_driver_read_timeout(mocker):
    mock = mocker.MagicMock()
    mock.get.side_effect = ReadTimeout()
    return mock


def test_scrap_page(mock_driver):
    """Testing mocked webdriver."""
    articles_to_retrieve = 50
    category_type=category_type = "nowe"
    url_with_item = "https://example.com"
    html_content = "<html><body><div>Mocked content</div></body></html>"
    mock_driver.page_source = html_content

    soup = ScrapPage(category_type=category_type, articles_to_retrieve=articles_to_retrieve)\
        .scrap_page(url_with_item, driver=mock_driver)

    assert soup is not None
    assert isinstance(soup, BeautifulSoup)
    assert soup.find("div").text == "Mocked content"

def test_connection_error(mock_driver_connection_error):
    """Testing mocked webdriver if raise ConnectionError."""
    articles_to_retrieve = 50
    category_type=category_type = "nowe"
    url_with_item = "https://example.com"

    with pytest.raises(ConnectionError) as exc_info:
        ScrapPage(category_type=category_type, articles_to_retrieve=articles_to_retrieve)\
        .scrap_page(url_with_item, driver=mock_driver_connection_error)

    assert "ConnectionError occured" in str(exc_info)

def test_missing_schema(mock_driver_missing_schema):
    """Testing mocked webdriver if raise MissingSchema."""
    articles_to_retrieve = 50
    category_type=category_type = "nowe"
    url_with_item = "https://example.com"

    with pytest.raises(MissingSchema) as exc_info:
        ScrapPage(category_type=category_type, articles_to_retrieve=articles_to_retrieve)\
        .scrap_page(url_with_item, driver=mock_driver_missing_schema)

    assert "MissingSchema occured" in str(exc_info)

def test_http_error(mock_driver_http_error):
    """Testing mocked webdriver if raise HTTPError."""
    articles_to_retrieve = 50
    category_type=category_type = "nowe"
    url_with_item = "https://example.com"

    with pytest.raises(HTTPError) as exc_info:
        ScrapPage(category_type=category_type, articles_to_retrieve=articles_to_retrieve)\
        .scrap_page(url_with_item, driver=mock_driver_http_error)

    assert "HTTPError occured" in str(exc_info)

def test_read_timeout(mock_driver_read_timeout):
    """Testing mocked webdriver if raise ReadTimeout."""
    articles_to_retrieve = 50
    category_type=category_type = "nowe"
    url_with_item = "https://example.com"

    with pytest.raises(ReadTimeout) as exc_info:
        ScrapPage(category_type=category_type, articles_to_retrieve=articles_to_retrieve)\
        .scrap_page(url_with_item, driver=mock_driver_read_timeout)

    assert "ReadTimeout occured" in str(exc_info)