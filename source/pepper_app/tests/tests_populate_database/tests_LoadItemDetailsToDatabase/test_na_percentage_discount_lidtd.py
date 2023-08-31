from pathlib import Path
import html5lib
import pytest
import datetime
import pandas as pd
from pepper_app.models import PepperArticle
from pepper_app.populate_database import LoadItemDetailsToDatabase



@pytest.fixture
def loaditemdetailstodatabase():
    item = [99999, "LG A1 55 cali", 3000.0, -10.0, 3300.0, "2023-08-31", "https://www.pepper.pl/promocje/lg-a1-55-719895"]
    return LoadItemDetailsToDatabase(item)


def test_na_percentage_discount_1(loaditemdetailstodatabase):
    """Test if function returns None if percentage discount is unknown."""
    row = pd.Series(data={'percentage_discount': 'NA'}, index=['percentage_discount'])
    output = loaditemdetailstodatabase.na_percentage_discount(row)

    assert output == None


def test_na_percentage_discount_2(loaditemdetailstodatabase):
    """Test if function returns correct value if percentage discount is known."""
    row = pd.Series(data={'percentage_discount': -10.0}, index=['percentage_discount'])
    output = loaditemdetailstodatabase.na_percentage_discount(row)

    assert output == -10.0


