from django.urls import path

from accounts.views import signup, settings

app_name = 'accounts'
urlpatterns = [
    path('signup/', signup.SignUpView.as_view(), name='signup'),
    path('activation/<str:activation_key>', signup.ActivationView.as_view(), name='activation'),
    path('settings/general/', settings.GeneralSettingsView.as_view(), name='settings_general'),
    path('settings/security/password', settings.PasswordChangeView.as_view(), name='settings_security_password')
]
