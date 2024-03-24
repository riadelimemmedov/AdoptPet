from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from config.helpers import is_valid_wallet_address

from .managers import CustomUserManager

# Create your models here.


# !CustomUser
class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = None
    email = models.EmailField(_("Email address"), unique=True, null=True)
    wallet_address = models.CharField(
        _("Wallet address"),
        unique=True,
        db_index=True,
        max_length=100,
        blank=True,
        null=True,
        validators=[is_valid_wallet_address],
    )
    is_staff = models.BooleanField(_("Is staff"), default=False)
    is_active = models.BooleanField(_("Is active"), default=True)
    date_joined = models.DateTimeField(_("Date joined"), default=timezone.now)
    username = models.CharField(_("Username"), max_length=100, unique=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("Custom user")
        verbose_name_plural = _("Custom users")
        ordering = ["-date_joined"]

    def __str__(self):
        return self.email
