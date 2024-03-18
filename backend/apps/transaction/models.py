from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel

from .validate_field import validate_confirmations, validate_from_user


# !Transaction
class Transaction(TimeStampedModel):
    from_user = models.CharField(_("from user"), max_length=100)
    confirmations = models.IntegerField(
        _("confirmations"), validators=[validate_confirmations]
    )
    value = models.CharField(_("value"), max_length=100)
    adopted_pet_slug = models.CharField(_("adopted slug"), max_length=100)

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"

    def __str__(self):
        return f"{self.from_user} -- {self.value} -- {self.value}"
