from __future__ import absolute_import, unicode_literals

from datetime import datetime, timedelta

from celery.schedules import crontab
from celery.task import periodic_task

from accounts.models import User
from opendataserver import settings


@periodic_task(run_every=(crontab(hour='0', minute='50')), ignore_result=True)
def delete_not_activated_accounts():
    User.objects.filter(
        is_active=False,
        date_joined__lt=datetime.now() - timedelta(days=settings.ACCOUNT_ACTIVATION_EXPIRY_DAYS)
    ).delete()
