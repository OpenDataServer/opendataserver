from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

from opendataserver import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'opendataserver.settings')

app = Celery('opendataserver')

app.config_from_object('django.conf:settings', namespace="CELERY")

app.autodiscover_tasks()

#
# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Calls test('hello') every 10 seconds.
#     sender.add_periodic_task(10.0, test.s(), name='add every 10')
#
#     # Calls test('world') every 30 seconds
#     sender.add_periodic_task(15.0, test.s(), expires=10)
#
#
# @app.task
# def test():
#     print("hello")