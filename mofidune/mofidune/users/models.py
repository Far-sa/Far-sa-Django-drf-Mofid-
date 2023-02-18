import datetime
from datetime import datetime, timedelta, timezone

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.translation import gettext as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.exceptions import NotAcceptable
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

User = get_user_model()


class Profile(models.Model):
    GENDER_MALE = "m"
    GENDER_FEMALE = "f"
    OTHER = "o"

    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (OTHER, "Other"),
    )

    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    # profile_picture = models.ImageField(upload_to=user_directory_path, blank=True)
    phone_number = PhoneNumberField(blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    about = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return "%s" % self.user.username

    @property
    def last_seen(self):
        return cache.get(f"seen_{self.user.username}")

    @property
    def online(self):
        if self.last_seen:
            now = datetime.now(timezone.utc)
            if now > self.last_seen + timedelta(minutes=settings.USER_ONLINE_TIMEOUT):
                return False
            else:
                return True
        else:
            return False


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.create(user=instance)


class PhoneNumber(models.Model):
    user = models.OneToOneField(User, related_name="phone", on_delete=models.CASCADE)
    phone_number = PhoneNumberField(unique=True)
    security_code = models.CharField(max_length=120)
    is_verified = models.BooleanField(default=False)
    sent = models.DateTimeField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.phone_number.as_e164

    def generate_security_code(self):
        """
        Returns a unique random `security_code` for given `TOKEN_LENGTH` in the settings.
        Default token length = 6
        """
        token_length = getattr(settings, "TOKEN_LENGTH", 6)
        return get_random_string(token_length, allowed_chars="0123456789")

    def is_security_code_expired(self):
        expiration_date = self.sent + datetime.timedelta(
            minutes=settings.TOKEN_EXPIRE_MINUTES
        )
        return expiration_date <= timezone.now()

    def send_confirmation(self):
        twilio_account_sid = settings.TWILIO_ACCOUNT_SID
        twilio_auth_token = settings.TWILIO_AUTH_TOKEN
        twilio_phone_number = settings.TWILIO_PHONE_NUMBER

        self.security_code = self.generate_security_code()

        # print(
        #     f'Sending security code {self.security_code} to phone {self.phone_number}')

        if all([twilio_account_sid, twilio_auth_token, twilio_phone_number]):
            try:
                twilio_client = Client(twilio_account_sid, twilio_auth_token)
                twilio_client.messages.create(
                    body=f"Your activation code is {self.security_code}",
                    to=str(self.phone_number),
                    from_=twilio_phone_number,
                )
                self.sent = timezone.now()
                self.save()
                return True
            except TwilioRestException as e:
                print(e)
        else:
            print("Twilio credentials are not set")

    def check_verification(self, security_code):
        if (
            not self.is_security_code_expired()
            and security_code == self.security_code
            and self.is_verified == False
        ):
            self.is_verified = True
            self.save()
        else:
            raise NotAcceptable(
                _(
                    "Your security code is wrong, expired or this phone is verified before."
                )
            )

        return self.is_verified


class Address(models.Model):
    user = models.ForeignKey(User, related_name="address", on_delete=models.CASCADE)
    country = CountryField(blank=False, null=False)
    city = models.CharField(max_length=100, blank=False, null=False)
    district = models.CharField(max_length=100, blank=False, null=False)
    street_address = models.CharField(max_length=250, blank=False, null=False)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    primary = models.BooleanField(default=False)
    phone_number = PhoneNumberField(null=True, blank=True)
    building_number = models.IntegerField(
        blank=True, null=True, validators=[MinValueValidator(1)]
    )
    apartment_number = models.IntegerField(
        blank=True, null=True, validators=[MinValueValidator(1)]
    )


class DeactivateUser(models.Model):
    user = models.OneToOneField(
        User, related_name="deactivate", on_delete=models.CASCADE
    )
    deactive = models.BooleanField(default=True)
