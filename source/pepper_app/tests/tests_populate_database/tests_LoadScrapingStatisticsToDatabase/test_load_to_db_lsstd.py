from pathlib import Path
import html5lib
import pytest
import datetime
from pytest_mock import mocker
from datetime import datetime, timedelta, date, timezone
from pepper_app.models import ScrapingStatistic
from pepper_app.populate_database import LoadScrapingStatisticsToDatabase


@pytest.fixture
def loadscrapingstatisticstodatabase():
    stats_info = ["nowe", 1, 50, datetime(2023, 8, 25, 12, 0, tzinfo=timezone.utc),
                timedelta(days =-1, seconds = 1), "NA", False, False, False, False]
    return LoadScrapingStatisticsToDatabase(stats_info)

@pytest.mark.django_db
def test_load_to_db_1(loadscrapingstatisticstodatabase):
    """Test loading stats_info into ScrapingStatistic table."""
    loadscrapingstatisticstodatabase.load_to_db()

    object_1 = ScrapingStatistic.objects.get(stats_id=1)


    assert object_1.category_type == "nowe"
    assert object_1.start_page == 1
    assert object_1.retrieved_articles_quantity == 50
    assert object_1.time_of_the_action == datetime(2023, 8, 25, 12, 0, tzinfo=timezone.utc)
    assert object_1.action_execution_datetime == timedelta(days =-1, seconds = 1)
    assert object_1.searched_article == None
    assert object_1.to_csv == False
    assert object_1.to_database == False
    assert object_1.scrap_continuously == False
    assert object_1.scrap_choosen_data == False

    object_1.delete()

