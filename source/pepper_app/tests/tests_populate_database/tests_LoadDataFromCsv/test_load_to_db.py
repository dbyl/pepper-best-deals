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
def test_load_to_db_1(loaddatafromcsv):

    input = Path("pepper_app/tests/fixtures/to_test_populate_database/scraped.csv")
    df = loaddatafromcsv.read_csv(input)
    loaddatafromcsv.load_to_db(df)

    object_1 = PepperArticle.objects.get(item_id=1000000)

    assert object_1.name == "Samsung S21"
    assert object_1.discount_price == 2000.0
    assert object_1.percentage_discount == -10.0
    assert object_1.regular_price == 2200.0
    assert object_1.date_added == datetime.date(2022, 7, 11)
    assert object_1.url == "https://www.pepper.pl/promocje/samsung-s21-714995"

    object_1.delete()


