from django.db import models

from django.utils import timezone
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from .user_manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(
        unique=True,
        max_length=255,
        blank=False,
    )

    username= models.CharField(
        _('User Name'),
        max_length=150,
        blank=True
    )

    first_name = models.CharField(
        _('first name'),
        max_length=30,
        blank=True,
    )
    last_name = models.CharField(
        _('last name'),
        max_length=150,
        blank=True,
    )

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into '
            'this admin site.'
        ),
    )

    is_active = models.BooleanField(
        _('active'),
        default=False,
        help_text=_(
            'Designates whether this user should be '
            'treated as active. Unselect this instead '
            'of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(
        _('date joined'),
        default=timezone.now,
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return f'[{self.id}] {self.email}'
        

class UserVerifyToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pincode = models.IntegerField(null=False, blank=False)
    created = models.DateTimeField(auto_now=True, auto_now_add=False)

from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "Click on the this link to reset password: {}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        subject="Password Reset for {title}".format(title="Some website title"),
        message=email_plaintext_message,
        from_email=None,
        recipient_list=[reset_password_token.user.email],
    )