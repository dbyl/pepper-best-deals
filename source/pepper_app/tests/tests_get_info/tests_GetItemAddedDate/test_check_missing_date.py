from pathlib import Path
import html5lib
import pytest
from bs4 import BeautifulSoup, Tag
from source.pepper_app.get_info import GetItemAddedDate

@pytest.fixture
def article():
    """Preparing article for tests."""
    path_to_file = Path("source/pepper_app/tests/fixtures/to_test_get_info/soup.html")
    with open(path_to_file, "r", encoding="utf-8") as file:
        soup = file.read()
    soup = BeautifulSoup(soup, "html5lib")
    articles = soup.find_all('article')
    article = articles[0] #Example article
    return article



def test_check_missing_date(article):
    """Test if function returns list with only 1 item "NA" """
    filtered_list = GetItemAddedDate(article).check_missing_date()

    assert len(filtered_list) == 1
    assert filtered_list[0] == "NA"
