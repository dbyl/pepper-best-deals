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
7) correct selenium setup inside a docker-container (to fix)
8) implementation of sample views along with celery task
9) implementation of auto-refreshing task status with javascript and redirecting when ready
10) implementation of basic bootstrap-based frontend 
11) implementation of scraping new articles
12) implementation of scraping of searched articles
13) improving searching articles by adding the feature to skip phrases provided by the user
14) fixing errors that occurred as a result of changes made to the scraped page
15) fixing errors that occurred as a result of changes made to the scraped page part 2
16) implementing user account creation with password recovery mechanism
17) implementing user requests with price email alert notifications
18) implementing article price history charts
19) updating functions (because of changes on pepper.pl)

## To fix/to do
1) updating unit tests
2) implementing html "soup" unit tests (checking if there have been changes to the provider's website)
3) docker 
4) ploting charts
5) ScrapingStatistic function - incorrect recording of statistics for continuous scraping
6) Adding comments, cleaning code (PEP8)
7) better frontend
8) updating README with pictures, gifs


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
POSTGRES_DB_ENGINE=django.db.backends.postgresql
POSTGRES_DB_NAME=your-postgres-name #generate your own postgres name
POSTGRES_USER=your-postgres-user #generate your own postgres user
POSTGRES_PASSWORD=your-postgres-password #generate your own postgres password
POSTGRES_HOST=host.docker.internal #change to localhost for running locally
ALLOWED_HOSTS=0.0.0.0,postgres,127.0.0.1,localhost
CELERY_BROKER_URL=redis://redis:6379 #change redis to localhost for running locally
CELERY_RESULT_BACKEND=redis://redis:6379
CELERY_ACCEPT_CONTENT=json
CELERY_TASK_SERIALIZER=json
CELERY_RESULT_SERIALIZER=json
CELERY_IGNORE_RESULT=False
CELERY_TRACK_STARTED=True
SELENIUM_CONTAINTER_NAME=selenium-hub
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

