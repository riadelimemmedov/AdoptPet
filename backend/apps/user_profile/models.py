from django.db import models
from django.db.models.signals import post_save
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django_extensions.db.fields import RandomCharField

from abstract.constants import Genders, Status, Types
from apps.users.models import CustomUser
from config.helpers import setFullName

# Create your models here.


# *ActiveQueryset
class ActiveQueryset(models.QuerySet):
    def get_is_active(self):
        return self.filter(is_active=True)

    def get_is_active_count(self):
        return self.filter(is_active=True).count()


# !Profile
class Profile(models.Model):
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

    objects = ActiveQueryset.as_manager()

    # photo = models.ImageField(
    #     _("Photo"),
    #     upload_to="account",
    #     blank=True,
    #     null=True,
    #     validators=[FileExtensionValidator(["png", "jpg", "jpeg"])],
    # )

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
            full_name = setFullName(
                self.first_name if self.first_name is not None else "",
                self.last_name if self.last_name is not None else "",
            )
            is_exists = __class__.objects.filter(full_name=full_name).exists()
            if is_exists:
                self.full_name = f"{full_name}_{self.profile_key}"
            else:
                self.full_name = f"{full_name}"
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
