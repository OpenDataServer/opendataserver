from __future__ import absolute_import, unicode_literals

from opendataserver import settings
from opendataserver.celery import app
from opendataserver.utils import get_influxdb_client


@app.task
def project_add_continuous_query(project_id: int):
    influxdb_client = get_influxdb_client()
    influxdb_client.create_continuous_query(
        name="project_" + str(project_id) + "_long_term",
        select='SELECT min("value") AS "min_peak", max("value") AS "max_peak", mean("value") AS "mean_value" INTO "long_term_data"."project_' + str(
            project_id) + '_long_term" FROM "raw_data"."project_' + str(project_id) + '_raw" GROUP BY time(1h), device_id, sensor_id',
        database=settings.INFLUXDB_DATABASE
    )
