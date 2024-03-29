from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models.signals import post_save
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django_extensions.db.fields import RandomCharField
from django_extensions.db.models import TimeStampedModel

from abstract.constants import Genders, Status, Types
from apps.users.models import CustomUser
from config.helpers import setFullName

# Create your models here.

User = get_user_model()


# *ActiveQueryset
class ActiveQueryset(models.QuerySet):
    def is_active(self):
        return self.filter(is_active=True)

    def is_active_count(self):
        return self.filter(is_active=True).count()


# *PassiveQueryset
class PassiveQueryset(models.QuerySet):
    def is_passive(self):
        return self.filter(is_active=False)

    def is_passive_count(self):
        return self.filter(is_active=False).count()


# *ProfileManager
class ProfileManager(models.Manager):
    def get_active_profiles(self):
        return ActiveQueryset(self.model, using=self._db)

    def get_passive_profiles(self):
        return PassiveQueryset(self.model, using=self._db)


# !Profile
class Profile(TimeStampedModel):
    user = models.OneToOneField(
        CustomUser, verbose_name=_("User"), on_delete=models.CASCADE, null=True
    )
    slug = models.SlugField(
        _("Slug"), unique=True, db_index=True, editable=False, blank=True
    )
    first_name = models.CharField(
        _("First name"), max_length=150, blank=True, null=True
    )
    last_name = models.CharField(_("Last name"), max_length=150, blank=True, null=True)
    full_name = models.CharField(_("Full name"), max_length=150, blank=True)
    profile_key = RandomCharField(
        _("Profile key"), length=12, unique=True, blank=True, include_alpha=True
    )
    country = models.CharField(verbose_name=_("Country"), max_length=50, blank=True)
    city = models.CharField(_("City"), max_length=50, null=True, blank=True)
    adress = models.CharField(_("Adress"), max_length=50, null=True, blank=True)
    additional_information = models.TextField(_("Additional Information"), blank=True)
    is_active = models.BooleanField(_("Is active"), default=False)

    objects = ProfileManager()

    profile_photo_url = models.FileField(
        _("Profile photo"),
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=["png", "jpg", "jpeg"])],
    )

    account_type = models.CharField(
        _("Account type"),
        max_length=20,
        choices=Types,
        default=Types[1][0],
        null=True,
        blank=False,
    )

    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=Status,
        default=Status[1][0],
        null=True,
        blank=False,
    )

    gender = models.CharField(
        _("Gender"), max_length=20, choices=Genders, null=True, blank=True
    )

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")

    def save(self, *args, **kwargs):
        if not self.full_name:
            # full_name = setFullName(
            #     self.first_name if self.first_name is not None else "",
            #     self.last_name if self.last_name is not None else "",
            # )
            is_exists = User.objects.filter(username=self.user.username).exists()
            if is_exists:
                self.full_name = f"{self.user.username}_{self.profile_key}"
            else:
                self.full_name = f"{self.user.username}"
            self.slug = slugify(self.full_name)
        super(Profile, self).save(*args, **kwargs)

    def get_full_name(self):
        return self.full_name

    def __str__(self):
        return self.full_name


# create_user_profile
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


post_save.connect(create_user_profile, CustomUser)
