from pathlib import Path
import html5lib
import pytest
from datetime import datetime
import pandas as pd
from pepper_app.models import PepperArticle
from pepper_app.populate_database import LoadDataFromCsv

@pytest.fixture
def loaddatafromcsv():
    return LoadDataFromCsv()


@pytest.mark.django_db
def test_read_csv_1(loaddatafromcsv):
    """Test reading csv file from given path."""
    path = Path("pepper_app/tests/fixtures/to_test_populate_database/scraped_test.csv")

    df = loaddatafromcsv.read_csv(path=path)

    assert isinstance(df, pd.DataFrame)

