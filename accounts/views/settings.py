from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext
from django.views.generic import UpdateView

from accounts.forms import GeneralUserChangeForm, PasswordChangeForm
from accounts.login_required import LoginRequiredMixin
from accounts.models import User


class GeneralSettingsView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = "settings/general.html"
    form_class = GeneralUserChangeForm
    model = User
    success_message = gettext("Your changes have been saved.")

    def get_success_url(self):
        return reverse_lazy("accounts:settings_general")

    def get_object(self, queryset=None):
        return self.request.user


class PasswordChangeView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = "settings/password.html"
    form_class = PasswordChangeForm
    model = User

    def get_success_url(self):
        return reverse_lazy("accounts:settings_security_password")

    def get_object(self, queryset=None):
        return self.request.user
