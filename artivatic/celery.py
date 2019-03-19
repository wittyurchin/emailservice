from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from django.conf import settings  # noqa

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'artivatic.settings')
app = Celery('artivatic', broker='amqp://guest@localhost//')
app.conf.update(
    CELERY_TASK_RESULT_EXPIRES=30,
)

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Using a string here means the worker will not have to
# pickle the object when using Windows.
# app.config_from_object('celeryconfig')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Celery will apply all configuration keys with defined namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# @app.task(bind=True)
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))


if __name__ == '__main__':
    app.start()
