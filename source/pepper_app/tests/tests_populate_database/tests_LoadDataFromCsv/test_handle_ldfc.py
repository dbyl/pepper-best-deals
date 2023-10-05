from pathlib import Path
import html5lib
import pytest
from datetime import datetime
from pepper_app.models import PepperArticle
from pepper_app.populate_database import LoadDataFromCsv



@pytest.fixture
def loaddatafromcsv():
    return LoadDataFromCsv()


@pytest.mark.django_db
def test_handle_1(loaddatafromcsv, monkeypatch, mocker):
    """Test if handle calls load_to_db function."""
    input = Path("source/pepper_app/tests/fixtures/to_test_populate_database/scraped_test.csv")
    load_to_db_mock = mocker.patch("pepper_app.populate_database.LoadDataFromCsv.load_to_db")

    loaddatafromcsv.handle(input=input)

    load_to_db_mock.assert_called_once()

