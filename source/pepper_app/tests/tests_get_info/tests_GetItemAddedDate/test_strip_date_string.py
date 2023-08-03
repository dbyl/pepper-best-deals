from pathlib import Path
import html5lib
import pytest
from bs4 import BeautifulSoup, Tag
from pepper_app.get_info import GetItemAddedDate
from pepper_app.tests.constans_for_tests import STRIPPED_DATE_STRINGS_TO_TEST_1, DESIRED_DATE_STRINGS_1


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


def test_strip_date_string():
    """Testing if function returns correctly trimmed date string."""
    for date_string_to_test, desired_date_string in zip(STRIPPED_DATE_STRINGS_TO_TEST_1, DESIRED_DATE_STRINGS_1):
        stripped_date_string_likely = GetItemAddedDate(article).strip_date_string(date_string_to_test)
        assert stripped_date_string_likely == desired_date_string

