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

exec(open("source/pepper_app/scrap_webpage_db.py").read())





