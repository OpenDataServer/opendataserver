from datetime import timedelta

from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core import signing
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import FormView

from accounts.exceptions import ActivationError
from accounts.forms import UserCreationForm
from accounts.models import User
from opendataserver import settings


class SignUpView(FormView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
    email_body_template = "activation_email_body.txt"

    def get_success_url(self, user=None):
        return super().get_success_url()

    def form_valid(self, form):
        return HttpResponseRedirect(self.get_success_url(self.register(form)))

    def create_inactive_user(self, form):
        new_user = form.save(commit=False)
        new_user.is_active = False
        new_user.save()

        return new_user

    def generate_activation_key(self, user):
        return signing.dumps(obj={
            "email": user.email,
            "sub": "account_activation"}
        )

    def send_activation_email(self, user):
        activation_key = self.generate_activation_key(user)
        context = {
            "scheme": "https" if self.request.is_secure() else "http",
            "activation_url": self.request.build_absolute_uri(reverse("accounts:activation", args=[activation_key])),
            "expiration_days": settings.ACCOUNT_ACTIVATION_EXPIRY_DAYS,
            "site": get_current_site(self.request),
            "user": user
        }
        subject = _("Please confirm your e-mail address")

        message = render_to_string(
            template_name=self.email_body_template,
            context=context,
            request=self.request,
        )
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=(user.email,)
        )

    def register(self, form):
        new_user = self.create_inactive_user(form)
        self.send_activation_email(new_user)
        messages.success(
            self.request,
            _("Thank you very much for your registration. We've sent you a confirmation mail with a link to activate "
              "your account."))
        return new_user


class ActivationView(View):
    SUCCESS_MESSAGE = _("You've activated your account successfully, you can now log in.")
    EXPIRED_MESSAGE = _("The account you attempted to activate has expired.")
    ALREADY_ACTIVATED_MESSAGE = _("The account is already activated. You can log in.")
    INVALID_KEY_MESSAGE = _("The activation key you provided is invalid.")

    def get(self, *args, **kwargs):
        try:
            self.activate_user(*args, **kwargs)
        except ActivationError as err:
            messages.error(self.request, err)
        else:
            messages.success(self.request, self.SUCCESS_MESSAGE)
        return redirect("login")

    def activate_user(self, *args, **kwargs):
        email = self.validate_key(kwargs.get("activation_key"))
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            raise ActivationError(self.EXPIRED_MESSAGE)
        if user.is_active:
            raise ActivationError(self.ALREADY_ACTIVATED_MESSAGE)
        else:
            user.is_active = True
            user.save()

    def validate_key(self, activation_key) -> str:
        try:
            activation_key_dec = signing.loads(
                activation_key,
                max_age=timedelta(days=settings.ACCOUNT_ACTIVATION_EXPIRY_DAYS)
            )
            if activation_key_dec['sub'] == "account_activation":
                return activation_key_dec['email']
            else:
                raise ActivationError(self.INVALID_KEY_MESSAGE)
        except signing.SignatureExpired:
            raise ActivationError(self.EXPIRED_MESSAGE)
        except signing.BadSignature:
            raise ActivationError(self.INVALID_KEY_MESSAGE)
