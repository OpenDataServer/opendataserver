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
    SENSOR_TYPES = [
        (gettext_lazy("Specific"), (
            ("air_pressure", gettext_lazy("Air pressure")),
            ("humidity", gettext_lazy("Humidity")),
            ("parking_lot", gettext_lazy("Parking lot (is free)")),
            ("particles_10", gettext_lazy("Particles PM10")),
            ("particles_2_5", gettext_lazy("Particles PM2.5")),
            ("radioactivity", gettext_lazy("Radioactivity")),
            ("rainfall", gettext_lazy("Rainfall")),
            ("temperature_indoor", gettext_lazy("Temperature (Indoor)")),
            ("temperature_outdoor", gettext_lazy("Temperature (Outdoor)")),
            ("water_level", gettext_lazy("Water level")),
            ("wind_speed", gettext_lazy("Wind speed")),
            ("wind_direction", gettext_lazy("Wind direction")),
            ("wind_gust", gettext_lazy("Wind gust")),
        )),
        (gettext_lazy("General"), (
            ("distance", gettext_lazy("Distance")),
            ("speed", gettext_lazy("Speed")),
        ))
    ]
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
        verbose_name="Sensor type",
        choices=SENSOR_TYPES
    )
    field_name_in_data = models.CharField(
        max_length=255,
        verbose_name="Field name in data"
    )
