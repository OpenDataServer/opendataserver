from django.forms import formset_factory
from django.shortcuts import render, redirect
from django.views.generic import FormView

from accounts.permissions import ProjectPermissionRequiredMixin, project_permission_required
from base.models import ProjectDevice, ProjectSensor
from data_sources.airrohr.forms.device_new import DeviceNewStep1Form, SensorNewForm, DeviceNewStep2Form
from data_sources.airrohr.models import ProjectAuthenticationAirrohr
from data_sources.airrohr.tasks import airrohr_data_get_raw_task


class DeviceNewStep1View(ProjectPermissionRequiredMixin, FormView):
    template_name = "device_new_step_1.html"
    form_class = DeviceNewStep1Form
    permission = "admin"

    def form_valid(self, form):
        return redirect("data_sources_airrohr:device_new_automatic_step_2", project_id=self.kwargs['project_id'],
                        sensor_id=form.cleaned_data['sensor_id'])


@project_permission_required(minimum_needed_permission="admin")
def device_new_step_2_view(request, project_id, sensor_id):
    if request.method == "GET":
        airrohr_data_raw = airrohr_data_get_raw_task.delay(sensor_id=sensor_id).get()
        SensorFormSet = formset_factory(SensorNewForm, extra=0)
        sensor_formset = SensorFormSet(
            initial=(
                {
                    "sensor_type": "particles_10",
                    "sensor_field_name": "P1"

                }, {
                    "sensor_type": "particles_2_5",
                    "sensor_field_name": "P2"
                }
            )
        )
        try:
            device_form = DeviceNewStep2Form(initial={
                "sensor_id": sensor_id,
                "geo_lat": float(airrohr_data_raw[0]['location']['latitude']),
                "geo_lon": float(airrohr_data_raw[0]['location']['longitude'])
            })
        except KeyError:
            device_form = DeviceNewStep2Form(initial={
                "sensor_id": sensor_id,
                "geo_lat": float(airrohr_data_raw[0]['location']['lat']),
                "geo_lon": float(airrohr_data_raw[0]['location']['long'])
            })
        return render(
            request=request,
            template_name="device_new_step_2.html",
            context={
                "sensor_formset": sensor_formset,
                "device_form": device_form
            }
        )

    elif request.method == "POST":
        SensorFormSet = formset_factory(SensorNewForm, extra=0)

        sensor_formset = SensorFormSet(request.POST)
        device_form = DeviceNewStep2Form(request.POST)

        if sensor_formset.is_valid() and device_form.is_valid():
            device = ProjectDevice.objects.create(
                name=device_form.cleaned_data['device_name'],
                data_source="airrohr",
                geo_lat=device_form.cleaned_data['geo_lat'],
                geo_lon=device_form.cleaned_data['geo_lon'],
                project_id=project_id,
            )
            for sensor_form_data in sensor_formset.cleaned_data:
                ProjectSensor.objects.create(
                    device=device,
                    name=sensor_form_data['sensor_name'],
                    type=sensor_form_data['sensor_type'],
                    field_name_in_data=sensor_form_data['sensor_field_name']
                )
            ProjectAuthenticationAirrohr.objects.create(
                device=device,
                sensor_id=sensor_id
            )
            return redirect("base:project_devices_list", project_id=project_id)

        else:
            return render(
                request=request,
                template_name="device_new_step_2.html",
                context={
                    "sensor_formset": sensor_formset,
                    "device_form": device_form
                }
            )
