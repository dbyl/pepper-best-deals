import os
import sys
from pathlib import Path
from pepper_app.environment_config import CustomEnvironment


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = CustomEnvironment.get_secret_key()

DEBUG = CustomEnvironment.get_debug()

ALLOWED_HOSTS = CustomEnvironment.get_allowed_hosts()

LOGGING = {
    "version": 1,
    "handlers": {"console": {"class": "logging.StreamHandler", "stream": sys.stdout}},
    "root": {"handlers": ["console"], "level": "DEBUG"},
    "loggers": {
        "asyncio": {
            "level": "WARNING",
        }}
}
6
LOGIN_URL = "login"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "pepper_app",
    "bootstrap5",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "configuration.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "configuration.wsgi.application"

DATABASES = {
        'default': {
            'ENGINE': CustomEnvironment.get_postgres_db_engine(),
            'NAME': CustomEnvironment.get_postgres_db_name(),
            'USER': CustomEnvironment.get_postgres_user(),
            'PASSWORD': CustomEnvironment.get_postgres_password(),
            'HOST': CustomEnvironment.get_postgres_host(),
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Warsaw"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CELERY_BROKER_URL = CustomEnvironment.get_celery_broker_url()
CELERY_RESULT_BACKEND = CustomEnvironment.get_celery_result_backend()
CELERY_ACCEPT_CONTENT = CustomEnvironment.get_celery_accept_content()
CELERY_TASK_SERIALIZER = CustomEnvironment.get_celery_task_serializer()
CELERY_RESULT_SERIALIZER = CustomEnvironment.get_celery_result_serializer()
CELERY_IGNORE_RESULT = CustomEnvironment.get_celery_ignore_result()
CELERY_TRACK_STARTED = CustomEnvironment.get_celery_track_started()

SESSION_SAVE_EVERY_REQUEST = True
SESSION_ENGINE = "django.contrib.sessions.backends.db"
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10200