# pepper-best-deals


# Pepper Best Deals

## Introduction

This django web application scrapes information from www.pepper.pl. Said site is a database of bargains, discounts of all kinds of products where individual bargains are created and rated by Users.
The purpose of the application is to collect informations about all deals, appearing on the site and to search historical data. Based on the scraped data, it will be possible to create a data warehouse.
Selected functions of the application that will be implemented:
1) Analysis of data for items, bargains selected by the user. For example, it will be possible to track the price of an item of interest.
2) The user will be able to define the item that interests him and set parameters such as price, name, discount. If the parameters are met, then he will receive an email/sms notification.
3) Constant scraping (deals hunting)

## Current stage of work

1) creating scraping functions based on Selenium and Beautifulsoup4
2) creating a django model (PepperArticle, ScrapingStatistic, UserRequest, SuccessfulResponse tables)
3) creating functions that populate the database (PepperArticle, ScrapingStatistic tables)
4) creating functions that save the scraped information to a csv file
5) creating more than 80 unit tests that test functions and validate the correctness of scraped data
6) implementation of a docker, creation of a PostgreSQL database, pgadmin4 panel
7) ...in progress...



## App Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/dbyl/pepper-best-deals
$ cd pepper-best-deals
```

This project requires Python 3.9 or later.

Create a virtual environment to install dependencies in and activate it:

Linux:
```sh
$ python3 -m venv env
$ source env/bin/activate
```

Create a .env file in project root directory (source). The file format can be understood from the example below:
```sh
DEBUG=True
SECRET_KEY=your-secret-key #generate your own secret key
URL=https://www.pepper.pl/
DATABASE_URL=postgres://postgres:postgres@host.docker.internal/postgres
ALLOWED_HOSTS=0.0.0.0,localhost
```

Application runs on docker so docker must be configured *(sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin)* and Docker Desktop must be installed.
Please open Docker Desktop and run docker-compose to install dependiences and run application:
```sh
(env)$ docker-compose -f docker-compose.yaml up --build
```

Docker-server should be started.

If project is setting up for the first time make sure that in source/pepper_app/migrations exists only one file - __init__.py.
To make migrations and create superuser open new terminal window and run:
```sh
(env)$ docker exec -it pepper_app /bin/bash
(env)$ python3 source/manage.py migrate
(env)$ python3 source/manage.py makemigrations
(env)$ python3 source/manage.py sqlmigrate pepper_app 0001
(env)$ python3 source/manage.py createsuperuser
(env)$ python3 source/manage.py migrate
```

To run tests run:
```sh
(env)$ python3 -m pytest source
```


celery -A configuration.celery worker --loglevel=INFO
redis-server
sudo service postgresql start
sudo -u postgres psql
sudo kill -9 10534
sudo -u postgres  psql second
ps -ef | grep postgres
python3 source/manage.py runserver 0.0.0.0:8000
pip install eventlet
celery -A configuration.celery worker --loglevel=info -P eventlet