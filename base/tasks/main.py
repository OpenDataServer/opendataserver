from celery.schedules import crontab
from celery.task import periodic_task

from accounts.models import User


@periodic_task(run_every=(crontab(minute='*')), name="some_task", ignore_result=True)
def some_task():
    return User.objects.get(email="me@leomaroni.de").first_name
