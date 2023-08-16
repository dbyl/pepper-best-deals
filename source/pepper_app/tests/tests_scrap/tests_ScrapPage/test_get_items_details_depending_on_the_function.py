from pathlib import Path
import html5lib
from pytest_mock import mocker
import time
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

def test_get_items_details_depending_on_the_function_1(monkeypatch, mocker):
    """Test get items details depending on the function whether the correct function has been started."""
    category_type = "nowe"
    articles_to_retrieve = 50
    scrap_continuously = False
    scrap_choosen_data = True

    def mock_sleep(seconds):
        pass

    monkeypatch.setattr(time, "sleep", mock_sleep)

    infinite_scroll_handling_mock = mocker.patch("pepper_app.scrap.ScrapPage.infinite_scroll_handling")
    get_items_details_mock = mocker.patch("pepper_app.scrap.ScrapPage.get_items_details")

    ScrapPage(category_type=category_type, articles_to_retrieve=articles_to_retrieve, \
        scrap_continuously=scrap_continuously, scrap_choosen_data=scrap_choosen_data).get_items_details_depending_on_the_function()

    get_items_details_mock.assert_called_once()
    infinite_scroll_handling_mock.assert_called_once()



def test_get_items_details_depending_on_the_function_2(monkeypatch, mocker):
    """Test get items details depending on the function whether the correct function has been started."""
    category_type = "nowe"
    articles_to_retrieve = 50
    scrap_continuously = True
    scrap_choosen_data = False

    def mock_sleep(seconds):
        pass

    monkeypatch.setattr(time, "sleep", mock_sleep)

    scrap_continuously_by_refreshing_page_mock = mocker.patch("pepper_app.scrap.ScrapPage.scrap_continuously_by_refreshing_page")
    get_items_details_mock = mocker.patch("pepper_app.scrap.ScrapPage.get_items_details")

    ScrapPage(category_type=category_type, articles_to_retrieve=articles_to_retrieve, \
        scrap_continuously=scrap_continuously, scrap_choosen_data=scrap_choosen_data).get_items_details_depending_on_the_function()
    
    scrap_continuously_by_refreshing_page_mock.assert_called_once()
    get_items_details_mock.assert_called_once()

"""
    def get_items_details_depending_on_the_function(self) -> None:
        if self.scrap_continuously == True and self.scrap_choosen_data == False:
            flag = True
            while flag == True:
                retrived_articles = self.scrap_continuously_by_refreshing_page()
                self.get_items_details(retrived_articles)
        elif self.scrap_continuously == False and self.scrap_choosen_data == True:
            retrived_articles = self.infinite_scroll_handling()
            self.get_items_details(retrived_articles)
        else:
            raise Exception(f"Matching get_items_details depending on the selected \
                            functionality failed. \n Tracking: {traceback.format_exc()}")
"""