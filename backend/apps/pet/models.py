from colorfield.fields import ColorField
from django.db import models
from django.utils.translation import gettext_lazy as _

from abstract.constants import GendersPet


# Create your models here.
# !Pet
class Pet(models.Model):
    name = models.CharField(_("Name"), max_length=50)
    age = models.IntegerField(_("Age"))
    breed = models.CharField(_("Breed"), max_length=50)
    color = ColorField()
    weight = models.FloatField(_("Weight"))
    gender = models.CharField(
        _("Gender"), choices=GendersPet, default=GendersPet[4][0], max_length=50
    )
    # image = models.ImageField(_("Image"), upload_to="images/")
    location = models.CharField(_("Location"), max_length=50)
    status = models.BooleanField(_("Status"), default=True)
    vaccinated = models.BooleanField(_("Vaccinated"), default=True)
    description = models.TextField(_("Description"), max_length=150)
