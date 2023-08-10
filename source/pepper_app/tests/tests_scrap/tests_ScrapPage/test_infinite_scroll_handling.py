from pathlib import Path
import html5lib
from pytest_mock import mocker

import pytest
from bs4 import BeautifulSoup, Tag
from pepper_app.scrap import ScrapPage

"""@pytest.fixture
def mock_select_url(mocker):
    mock = mocker.MagicMock()
    mock.return_value = "https://www.pepper.pl/nowe?page=1"
    return mock"""

@pytest.fixture
def soup():
    """Preparing article for tests."""
    path_to_file = Path("pepper_app/tests/fixtures/to_test_scrap/soup.html")
    with open(path_to_file, "r", encoding="utf-8") as file:
        soup = file.read()
    soup = BeautifulSoup(soup, "html5lib")
    return soup



def test_infinite_scroll_handling_1(mocker, soup):
    """ Comm """
    scrap_continuously = False
    category_type = "nowe"
    articles_to_retrieve = 50

    select_url_mocked_value = "https://www.pepper.pl/nowe?page=1"
    scrap_page_mocked_value = soup

    select_url_mock = mocker.patch("pepper_app.scrap.ScrapPage.select_url")
    select_url_mock.return_value = select_url_mocked_value

    scrap_page_mock = mocker.patch("pepper_app.scrap.ScrapPage.scrap_page")
    scrap_page_mock.return_value = scrap_page_mocked_value

    retrived_articles = ScrapPage(category_type=category_type, articles_to_retrieve=articles_to_retrieve).infinite_scroll_handling()

    assert isinstance(retrived_articles, list)
    assert ScrapPage(category_type=category_type, articles_to_retrieve=articles_to_retrieve).select_url() == "dd"





"""
   def infinite_scroll_handling(self) -> List[str]:
        try:
            flag = True
            retrived_articles = list()
            while flag:
                url_to_scrap = self.select_url()
                soup = self.scrap_page(url_to_scrap)
                flag = CheckConditions(soup).check_if_last_page_nowe()
                flag = CheckConditions(soup).check_if_last_page_search()
                if flag == False:
                    return retrived_articles[:self.articles_to_retrieve]
                flag = CheckConditions(soup).check_if_no_items_found()
                if flag == False:
                    return retrived_articles[:self.articles_to_retrieve]
                if flag == True:
                    articles = soup.find_all('article')
                    retrived_articles += articles
                else:
                    return retrived_articles[:self.articles_to_retrieve]
                if len(retrived_articles) >= self.articles_to_retrieve:
                    flag = False
                    return retrived_articles[:self.articles_to_retrieve]
                self.start_page += 1
        except Exception as e:
            raise Exception(f"Infinite scroll failed:\
                            {e}\n Tracking: {traceback.format_exc()}")
"""