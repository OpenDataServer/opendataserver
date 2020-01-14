# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from data_sources.airrohr.signals import airrohr_periodic_task_signal


class Command(BaseCommand):
    help = 'Runs the periodical tasks of the airrohr datasource'

    def handle(self, *args, **options):
        airrohr_periodic_task_signal.send(self)
