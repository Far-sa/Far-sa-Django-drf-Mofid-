from dj_rest_auth.registration.views import ResendEmailVerificationView, VerifyEmailView
from dj_rest_auth.views import (
    LogoutView,
    PasswordChangeView,
    PasswordResetConfirmView,
    PasswordResetView,
)
from django.urls import include, path
from django.views.generic import TemplateView

from .views import (
    GoogleLogin,
    SendOrResendSMSAPIView,
    UserLoginAPIView,
    UserRegisterationAPIView,
    VerifyPhoneNumberAPIView,
)

app_name = "users"

urlpatterns = [
    path("register/", UserRegisterationAPIView.as_view(), name="user_register"),
    path("login/", UserLoginAPIView.as_view(), name="user_login"),
    path("send-sms/", SendOrResendSMSAPIView.as_view(), name="send_resend_sms"),
    path(
        "verify-phone/", VerifyPhoneNumberAPIView.as_view(), name="verify_phone_number"
    ),
    ######
    path(
        "resend-email/", ResendEmailVerificationView.as_view(), name="rest_resend_email"
    ),
    path(
        "account-confirm-email/(?P<key>[-:\w]+)/$",
        VerifyEmailView.as_view(),
        name="account_confirm_email",
    ),
    path(
        "account-email-verification-sent/",
        TemplateView.as_view(),
        name="account_email_verification_sent",
    ),
    # path('login/google/', GoogleLogin.as_view(), name='google_login'),
    path("password/reset/", PasswordResetView.as_view(), name="rest_password_reset"),
    path(
        "password/reset/confirm/<str:uidb64>/<str:token>",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path("password/change/", PasswordChangeView.as_view(), name="rest_password_change"),
    path("logout/", LogoutView.as_view(), name="rest_logout"),
]
