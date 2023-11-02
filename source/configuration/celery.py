import os
import time
from celery import Celery
from django.conf import settings
from django.apps import apps
from celery.exceptions import Ignore


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "configuration.settings")

app = Celery("configuration", include=['pepper_app.tasks'])

app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.task_track_started = True
app.conf.task_ignore_result = False

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


