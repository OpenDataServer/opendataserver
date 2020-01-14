from django.db import models

from base.models import ProjectDevice


class ProjectAuthenticationTTN(models.Model):
    device = models.ForeignKey(
        to=ProjectDevice,
        on_delete=models.CASCADE,
        verbose_name="Device"
    )
    app_id = models.CharField(
        max_length=255,
        verbose_name="Application ID (by TTN)"
    )
    access_key = models.CharField(
        max_length=255,
        verbose_name="Access key (by TTN)"
    )
    discovery_address = models.CharField(
        max_length=255,
        default="discovery.thethings.network:1900"
    )
