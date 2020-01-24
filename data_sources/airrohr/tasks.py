import requests
from django.dispatch import receiver

from base.models import ProjectSensor
from data_sources.airrohr.models import ProjectAuthenticationAirrohr
from data_sources.airrohr.signals import airrohr_periodic_task_signal
from opendataserver.celery import app
from opendataserver.utils import get_influxdb_client


def data_get_raw(sensor_id):
    with requests.Session() as session:
        r = session.get("http://api.luftdaten.info/static/v1/sensor/" + str(sensor_id) + "/")
        data = r.json()
        return data


@app.task()
def airrohr_data_get_raw_task(sensor_id):
    return data_get_raw(sensor_id=sensor_id)


@app.task()
def airrohr_data_get_task(authentication_airrohr_id: int):
    authentication_airrohr = ProjectAuthenticationAirrohr.objects.get(pk=authentication_airrohr_id)
    influxdb_client = get_influxdb_client()
    data_raw = data_get_raw(authentication_airrohr.sensor_id)
    influxdb_data_points = []
    for data_point in data_raw:
        for sensor_data_value in data_point['sensordatavalues']:
            sensor = ProjectSensor.objects.filter(
                device=authentication_airrohr.device,
                field_name_in_data=sensor_data_value['value_type']
            ).first()
            influxdb_data_points.append({
                "measurement": "project_" + str(authentication_airrohr.device.project.pk) + "_raw",
                "tags": {
                    "device_id": authentication_airrohr.device.pk,
                    "sensor_id": sensor.pk
                },
                "retention_policy": "raw_data",
                "time": data_point['timestamp'],
                "fields": {
                    "value": sensor_data_value['value']
                }
            })
        influxdb_client.write_points(influxdb_data_points)


@receiver(signal=airrohr_periodic_task_signal)
def airrohr_data_get_periodic_manager(sender, **kwargs):
    for authentication_airrohr in ProjectAuthenticationAirrohr.objects.all():
        airrohr_data_get_task.apply_async(args=(authentication_airrohr.pk,))
