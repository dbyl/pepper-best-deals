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

def test_get_items_details_depending_on_the_function_1(mocker, soup):
    """Test get items details depending on the function whether the correct function has been started."""
    category_type = "nowe"
    articles_to_retrieve = 50
    scrap_continuously = True
    scrap_choosen_data = False

    scrap_continuously_by_refreshing_page_mock = mocker.patch("pepper_app.scrap.ScrapPage.scrap_continuously_by_refreshing_page")
    infinite_scroll_handling_mock = mocker.patch("pepper_app.scrap.ScrapPage.infinite_scroll_handling")
    get_items_details_mock = mocker.patch("pepper_app.scrap.ScrapPage.get_items_details")



    scrap_continuously_by_refreshing_page_mock.return_value = "the function scrap_continuously_by_refreshing_page has been called"
    infinite_scroll_handling_mock.return_value = "the function infinite_scroll_handling has been called"
    get_items_details_mock.return_value = "the function get_items_details has been called"

    ScrapPage(category_type=category_type, articles_to_retrieve=articles_to_retrieve, \
        scrap_continuously=scrap_continuously, scrap_choosen_data=scrap_choosen_data).get_items_details_depending_on_the_function()


    assert retrived_articles == "the function scrap_continuously_by_refreshing_page has been called"
    #assert get_items_details_mock.assert_called_once_with(retrived_articles)

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