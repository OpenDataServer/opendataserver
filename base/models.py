from django.db import models
from django.utils.translation import gettext_lazy


class Project(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Project Name'
    )


class ProjectMember(models.Model):
    ROLES = [
        ('owner', gettext_lazy('Owner')),
        ('admin', gettext_lazy('Admin')),
        ('member', gettext_lazy('Member')),
        ('restricted', gettext_lazy('Restricted')),
    ]

    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        to='accounts.User',
        on_delete=models.CASCADE
    )

    role = models.CharField(
        verbose_name='Role',
        max_length=255,
        choices=ROLES,
    )


class ProjectDevice(models.Model):
    DATA_SOURCES = [
        ("ttn", "The Things Network"),
        ("airrohr", "Airrohr/Luftdaten.info")
    ]
    name = models.CharField(
        max_length=255,
        verbose_name="Name"
    )
    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        verbose_name="Project"
    )
    data_source = models.CharField(
        max_length=255,
        choices=DATA_SOURCES,
        verbose_name="Data source"
    )
    geo_lat = models.FloatField(
        verbose_name="Latitude"
    )
    geo_lon = models.FloatField(
        verbose_name="Longitude"
    )


class ProjectSensor(models.Model):
    device = models.ForeignKey(
        to=ProjectDevice,
        on_delete=models.CASCADE,
        verbose_name="Device"
    )
    name = models.CharField(
        max_length=255,
        verbose_name="Name"
    )
    type = models.CharField(
        max_length=255,
        verbose_name="Sensor type"
    )
    field_name_in_data = models.CharField(
        max_length=255,
        verbose_name="Field name in data"
    )