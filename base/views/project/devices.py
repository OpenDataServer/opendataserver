from django.views.generic import TemplateView

from base.models import ProjectSensor, ProjectDevice


class DevicesList(TemplateView):
    template_name = "project/devices/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        devices_ctx_list = []
        devices = ProjectDevice.objects.filter(project_id=kwargs['project_id'])
        for device in devices:
            sensors = ProjectSensor.objects.filter(device=device)
            devices_ctx_list.append({
                "name": device.name,
                "sensor_count": sensors.count()
            })
        context['devices'] = devices_ctx_list
        return context
