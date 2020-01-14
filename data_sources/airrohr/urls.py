from django.urls import path

from data_sources.airrohr.views import device_new

app_name = 'data_sources_airrohr'

urlpatterns = [
    path("device/new/", device_new.DeviceNewStep1View.as_view(), name="device_new"),
    path("device/new/<int:sensor_id>/automatic/", device_new.device_new_step_2_view,
         name="device_new_automatic_step_2"),
]
