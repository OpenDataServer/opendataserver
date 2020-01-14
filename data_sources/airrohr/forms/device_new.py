from django import forms
from django.utils.translation import gettext_lazy

from base.models import ProjectSensor


class DeviceNewStep1Form(forms.Form):
    sensor_id = forms.IntegerField(
        label=gettext_lazy("Sensor ID (given by Airrohr)"),
        required=True,
        widget=forms.NumberInput(
            attrs={
                'required': ''
            }
        )
    )


class DeviceNewStep2Form(forms.Form):
    sensor_id = forms.IntegerField(
        required=True,
        widget=forms.HiddenInput()
    )

    device_name = forms.CharField(
        label=gettext_lazy("Device name"),
        required=True,
        widget=forms.TextInput(
            attrs={
                'required': ''
            }
        ),
        error_messages={
            "required": gettext_lazy("Please enter a device name")
        }
    )

    geo_lat = forms.FloatField(
        label=gettext_lazy("Latitude"),
        widget=forms.NumberInput(
            attrs={
                'class': 'input',
                'step': 'any'
            }
        )
    )

    geo_lon = forms.FloatField(
        label=gettext_lazy("Longitude"),
        widget=forms.NumberInput(
            attrs={
                'class': 'input',
                'step': 'any'
            }
        ),
    )


class SensorNewForm(forms.Form):
    sensor_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'placeholder': gettext_lazy("Sensor name"),
                'class': 'input',
                'required': ""
            }
        ),
        required=True,
        error_messages={
            "required": gettext_lazy("Please enter a name for all sensors")
        }
    )
    sensor_type = forms.ChoiceField(
        choices=ProjectSensor.SENSOR_TYPES,
        required=True
    )
    sensor_field_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'placeholder': gettext_lazy("Field name in data"),
                'class': 'input',
                'required': ''
            }
        ),
        required=True,
        error_messages={
            "required": gettext_lazy("Please enter a data field name for all sensors")
        }
    )
