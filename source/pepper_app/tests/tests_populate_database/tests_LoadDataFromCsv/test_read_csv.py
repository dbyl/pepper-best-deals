from pathlib import Path
import html5lib
import pytest
from datetime import datetime
from pepper_app.models import PepperArticle
from pepper_app.populate_database import LoadDataFromCsv

@pytest.fixture
def loaddatafromcsv():
    return LoadDataFromCsv()

def test_read_csv():