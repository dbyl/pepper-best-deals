# pepper-best-deals

clean cache, migrations

sudo -u postgres psql
\dt
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

sudo service postgresql start

python source/manage.py flush
python source/manage.py makemigrations pepper_app
python source/manage.py migrate
python source/manage.py sqlmigrate pepper_app 0001
python source/manage.py createsuperuser

python source/manage.py migrate pepper_app

python source/manage.py runserver

new_terminal
python source/manage.py shell

exec(open("source/pepper_app/scrap.py").read())




git commit -m "Implementing tests for get_info -> GetItemId, GetItemName, GetItemDiscountPrices"
pytest --ds=configuration.settings


pytest pepper_app/tests/tests_scrap/tests_ScrapPage/test_scrap_continuously_by_refreshing_page.py --ds=configuration.settings
pytest pepper_app/tests/tests_scrap/tests_ScrapPage/test_get_items_details_depending_on_the_function.py --ds=configuration.settings
pytest pepper_app/tests/tests_scrap/tests_ScrapPage/test_signal_handler_for_continuously_scrapping.py --ds=configuration.settings

