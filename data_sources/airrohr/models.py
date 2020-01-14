from django.db import models

from base.models import ProjectDevice


class ProjectAuthenticationAirrohr(models.Model):
    device = models.ForeignKey(
        to=ProjectDevice,
        on_delete=models.CASCADE,
        verbose_name="Device"
    )
    sensor_id = models.CharField(
        max_length=255,
        verbose_name="Sensor ID (by Airrohr)"
    )
