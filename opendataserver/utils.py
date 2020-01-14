from django.conf import settings

from influxdb import InfluxDBClient


def get_influxdb_client():
    return InfluxDBClient(
        host=settings.INFLUXDB_HOST,
        port=settings.INFLUXDB_PORT,
        username=settings.INFLUXDB_USERNAME,
        password=settings.INFLUXDB_PASSWORD,
        database=settings.INFLUXDB_DATABASE,
        ssl=settings.INFLUXDB_SSL,
        verify_ssl=settings.INFLUXDB_VERIFY_SSL
    )
