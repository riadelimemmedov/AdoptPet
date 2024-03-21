from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel

from abstract.constants import PaymentOptions


# !Transaction
class Transaction(TimeStampedModel):
    from_user = models.CharField(_("from user"), max_length=100)
    confirmations = models.IntegerField(_("confirmations"), null=True)
    value = models.CharField(_("value"), max_length=100)
    adopted_pet_slug = models.CharField(
        _("adopted slug"), unique=True, db_index=True, max_length=100
    )
    payment_options = models.CharField(
        _("payment options"), max_length=100, choices=PaymentOptions
    )
    session_id = models.CharField(_("session"), max_length=100, null=True)

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"

    def save(self, *args, **kwargs):
        self.from_user = self.from_user.lower()
        super(Transaction, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.from_user} -- {self.value} -- {self.payment_options}"
