from pathlib import Path
import html5lib
import pytest
from bs4 import BeautifulSoup, Tag
from source.pepper_app.get_info import GetItemAddedDate
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from requests.exceptions import ConnectionError, MissingSchema, HTTPError, ReadTimeout




@pytest.fixture
def article():
    """Preparing article for tests."""
    path_to_file = Path("source/pepper_app/tests/fixtures/to_test_get_info/soup.html")
    with open(path_to_file, "r", encoding="utf-8") as file:
        soup = file.read()
    soup = BeautifulSoup(soup, "html5lib")
    articles = soup.find_all('article')
    article = articles[1] #Example article
    return article

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


def test_scrape_page(mock_driver):
    """Testing mocked webdriver."""
    url_with_item = "https://example.com"
    html_content = "<html><body><div>Mocked content</div></body></html>" 
    mock_driver.page_source = html_content 
 
    soup = GetItemAddedDate(article).scrape_page(url_with_item, driver=mock_driver)

    assert soup is not None
    assert isinstance(soup, BeautifulSoup)
    assert soup.find("div").text == "Mocked content"

def test_connection_error(mock_driver_connection_error):
    """Testing mocked webdriver if raise ConnectionError."""
    url_with_item = "https://example.com"

    with pytest.raises(ConnectionError) as exc_info:
        GetItemAddedDate(article).scrape_page(url_with_item, driver=mock_driver_connection_error)

    assert "ConnectionError occured" in str(exc_info)

def test_missing_schema(mock_driver_missing_schema):
    """Testing mocked webdriver if raise MissingSchema."""
    url_with_item = "https://example.com"

    with pytest.raises(MissingSchema) as exc_info:
        GetItemAddedDate(article).scrape_page(url_with_item, driver=mock_driver_missing_schema)

    assert "MissingSchema occured" in str(exc_info)

def test_http_error(mock_driver_http_error):
    """Testing mocked webdriver if raise HTTPError."""
    url_with_item = "https://example.com"

    with pytest.raises(HTTPError) as exc_info:
        GetItemAddedDate(article).scrape_page(url_with_item, driver=mock_driver_http_error)

    assert "HTTPError occured" in str(exc_info)

def test_read_timeout(mock_driver_read_timeout):
    """Testing mocked webdriver if raise ReadTimeout."""
    url_with_item = "https://example.com"

    with pytest.raises(ReadTimeout) as exc_info:
        GetItemAddedDate(article).scrape_page(url_with_item, driver=mock_driver_read_timeout)

    assert "ReadTimeout occured" in str(exc_info)