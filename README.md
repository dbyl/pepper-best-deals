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
pytest pepper_app/tests/tests_scrap/tests_ScrapPage/test_get_items_details.py --ds=configuration.settings
pytest pepper_app/tests/tests_scrap/tests_ScrapPage/test_signal_handler_for_continuously_scrapping.py --ds=configuration.settings

pytest pepper_app/tests/tests_scrap/tests_ScrapPage/test_signal_handler_for_continuously_scrapping.py --ds=configuration.settings

pytest pepper_app/tests/tests_scrap/tests_ScrapPage/test_get_scraping_stats_info.py --ds=configuration.settings


pytest pepper_app/tests/tests_populate_database/tests_LoadDataFromCsv/test_handle.py --ds=configuration.settings
pytest pepper_app/tests/tests_populate_database/tests_LoadItemDetailsToDatabase/test_load_to_db_lidtd.py --ds=configuration.settings

pytest pepper_app/tests/tests_article_and_soup/test_soup.py --ds=configuration.settings



docker exec -it pepper-best-deals-web-1 sh -c "pytest"

docker exec -t -i pepper-best-deals-web-1 sh /bin/bash
docker exec -it pepper-best-deals-web-1 sh -c "python3 -m pytest source"
docker exec -it pepper-best-deals-web-1 sh -c "python3 -m pytest source"
docker exec -it pepper-best-deals-web-1 sh -c "python3 source/manage.py createsuperuser"