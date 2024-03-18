from django import forms
from django.contrib import admin

from .models import Transaction
from .validate_field import validate_confirmations, validate_from_user

# Register your models here.


# * TransactionModelForm
class TransactionModelForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        confirmations = cleaned_data.get("confirmations")
        from_user = cleaned_data.get("from_user")
        if len(cleaned_data) == 0:
            return
        if not validate_confirmations(confirmations):
            self.add_error("confirmations", "Confirmations value 1 or 0")
        if not validate_from_user(from_user):
            self.add_error("from_user", "Please input valid wallet address")


# !TransactionalAdmin
class TransactionalAdmin(admin.ModelAdmin):
    form = TransactionModelForm
    list_display = [
        "from_user",
        "confirmations",
        "value",
        "adopted_pet_slug",
        "created",
        "modified",
    ]
    list_display_links = ["from_user", "confirmations"]


admin.site.register(Transaction, TransactionalAdmin)
