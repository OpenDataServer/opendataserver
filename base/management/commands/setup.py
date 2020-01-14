# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from opendataserver import settings
from opendataserver.utils import get_influxdb_client


class Command(BaseCommand):
    help = 'Runs the setup process'

    def handle(self, *args, **options):
        influxdb_client = get_influxdb_client()

        influxdb_client.create_database(settings.INFLUXDB_DATABASE)

        influxdb_client.create_retention_policy(
            name="raw_data",
            duration="4w",
            replication=settings.INFLUXDB_REPLICATION_FACTOR
        )
        influxdb_client.create_retention_policy(
            name="long_term_data",
            duration="52w",
            replication=settings.INFLUXDB_REPLICATION_FACTOR
        )
