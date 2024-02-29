from colorfield.fields import ColorField
from django.core.cache import cache
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django_extensions.db.fields import RandomCharField
from django_extensions.db.models import TimeStampedModel
from django_lifecycle import (
    AFTER_DELETE,
    AFTER_SAVE,
    AFTER_UPDATE,
    LifecycleModel,
    hook,
)

from abstract.constants import GendersPet
from config.helpers import setPetName


# *ActiveStatusQueryset
class ActiveStatusQueryset(models.QuerySet):
    def active_status(self):
        return self.filter(status=True)

    def active_status_count(self):
        return self.filter(status=True).count()


# *PassiveStatusQueryset
class PassiveStatusQueryset(models.QuerySet):
    def passive_status(self):
        return self.filter(status=False)

    def passive_status_count(self):
        return self.filter(status=False).count()


# ?PetManager
class PetManager(models.Manager):
    def get_active_status(self):
        return ActiveStatusQueryset(self.model, using=self._db)

    def get_passive_status(self):
        return PassiveStatusQueryset(self.model, using=self._db)


# Create your models here.
# !Pet
class Pet(TimeStampedModel, LifecycleModel):
    name = models.CharField(_("Name"), max_length=50)
    age = models.IntegerField(_("Age"))
    breed = models.CharField(_("Breed"), max_length=50)
    slug = models.SlugField(
        _("Slug"), unique=True, db_index=True, editable=False, blank=True
    )
    pet_key = RandomCharField(
        _("Pet key"), length=12, unique=True, blank=True, include_alpha=True
    )
    color = ColorField()
    weight = models.FloatField(_("Weight"))
    gender = models.CharField(
        _("Gender"), choices=GendersPet, default=GendersPet[4][0], max_length=50
    )
    pet_photo_url = models.FileField(
        _("Pet photo"),
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    "png",
                    "jpg",
                    "jpeg",
                ]
            )
        ],
    )
    location = models.CharField(_("Location"), max_length=50)
    city = models.CharField(_("City"), max_length=50)
    status = models.BooleanField(_("Status"), default=True)
    vaccinated = models.BooleanField(_("Vaccinated"), default=True)
    description = models.TextField(_("Description"), max_length=150)

    objects = PetManager()

    class Meta:
        verbose_name = _("Pet")
        verbose_name_plural = _("Pets")
        ordering = ["-created"]

    def save(self, *args, **kwargs):
        slug_data = f"{self.name}-{self.pet_key}"
        self.slug = slugify(slug_data)
        super(Pet, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.age}"

    @hook(AFTER_SAVE)
    @hook(AFTER_DELETE)
    @hook(AFTER_UPDATE)
    def invalidate_cache(self):
        cache.delete("pet_objects")
