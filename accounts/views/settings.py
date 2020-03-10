from datetime import timedelta

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core import signing
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import UpdateView, FormView

from accounts.exceptions import ActivationError
from accounts.forms import GeneralUserChangeForm, PasswordChangeForm, EmailChangeForm
from accounts.login_required import LoginRequiredMixin
from accounts.models import User
from opendataserver import settings


class GeneralSettingsView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = "settings/general.html"
    form_class = GeneralUserChangeForm
    model = User
    success_message = _("Your changes have been saved.")

    def get_success_url(self):
        return reverse_lazy("accounts:settings_general")

    def get_object(self, queryset=None):
        return self.request.user


class EmailChangeView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    template_name = "settings/email.html"
    form_class = EmailChangeForm
    success_url = reverse_lazy("accounts:settings_general_email")
    email_body_template = "settings/email_change_confirmation_body.txt"

    @cached_property
    def add_form(self):
        return EmailChangeForm(data=(self.request.POST if self.request.method == "POST" else None))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = self.add_form
        return ctx

    def generate_confirm_key(self, new_email: str):
        return signing.dumps(obj={
            "email": self.request.user.email,
            "new_email": new_email,
            "sub": "account_settings_email_change_confirm"}
        )

    def send_confirm_email(self, new_email: str):
        confirm_key = self.generate_confirm_key(new_email)
        context = {
            "activation_url": self.request.build_absolute_uri(
                reverse(
                    "accounts:settings_general_email_confirm_change",
                    args=[confirm_key]
                )
            ),
            "site": get_current_site(self.request),
            "expiration_days": settings.CONFIRMATION_EXPIRY_DAYS,
            "user": self.request.user
        }
        subject = _("Please confirm your new e-mail address")

        message = render_to_string(
            template_name=self.email_body_template,
            context=context,
            request=self.request,
        )
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=(new_email,)
        )

    def form_valid(self, form):
        self.send_confirm_email(form.cleaned_data["email"])
        messages.success(
            self.request,
            _("We've send you an e-mail to confirm your new e-mail address. "
              "Please click the link in the e-mail to make your change effective."))
        return HttpResponseRedirect(self.get_success_url())


class EmailChangeConfirmView(View):
    SUCCESS_MESSAGE = _("Your e-mail address has been changed.")
    EXPIRED_MESSAGE = _("The confirmation key you provided has expired. Please request a new link.")
    ALREADY_CONFIRMED_MESSAGE = _("The e-mail address is already confirmed.")
    INVALID_KEY_MESSAGE = _("The confirmation key you provided is invalid.")
    email_notification_body_template = "settings/email_notification_body.txt"

    def get(self, *args, **kwargs):
        try:
            self.confirm_email_change(*args, **kwargs)
        except ActivationError as err:
            messages.error(self.request, err)
        else:
            messages.success(self.request, self.SUCCESS_MESSAGE)
        return redirect("accounts:settings_general")

    def send_notification_email(self, new_email: str, user: User):
        context = {
            "support_email_address": settings.SUPPORT_EMAIL_ADDRESS,
            "new_email": new_email
        }
        subject = _("Your e-mail address has been changed")

        message = render_to_string(
            template_name=self.email_notification_body_template,
            context=context,
            request=self.request,
        )
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=(user.email,)
        )

    def confirm_email_change(self, *args, **kwargs):
        decrypted_confirm_key = self.decrypt_key(kwargs.get("confirm_key"))
        try:
            user = User.objects.get(email=decrypted_confirm_key["email"])
        except ObjectDoesNotExist:
            raise ActivationError(self.EXPIRED_MESSAGE)
        if user.email == decrypted_confirm_key["new_email"]:
            raise ActivationError(self.ALREADY_CONFIRMED_MESSAGE)
        else:
            self.send_notification_email(
                new_email=decrypted_confirm_key["new_email"],
                user=user
            )
            user.email = decrypted_confirm_key["new_email"]
            user.save()

    def decrypt_key(self, confirm_key) -> dict:
        try:
            confirm_key_dec = signing.loads(
                confirm_key,
                max_age=timedelta(days=settings.CONFIRMATION_EXPIRY_DAYS)
            )
            if confirm_key_dec['sub'] == "account_settings_email_change_confirm":
                return confirm_key_dec
            else:
                raise ActivationError(self.INVALID_KEY_MESSAGE)
        except signing.SignatureExpired:
            raise ActivationError(self.EXPIRED_MESSAGE)
        except signing.BadSignature:
            raise ActivationError(self.INVALID_KEY_MESSAGE)


class PasswordChangeView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = "settings/password.html"
    form_class = PasswordChangeForm
    model = User

    def get_success_url(self):
        return reverse_lazy("accounts:settings_security_password")

    def get_object(self, queryset=None):
        return self.request.user
