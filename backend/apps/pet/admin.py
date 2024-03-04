from django import forms
from django.contrib import admin

from .models import Pet


# ?PetAdminForm
class PetAdminForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        # Perform your custom validation here
        pet_photo_url = cleaned_data.get("pet_photo_url")
        pet_photo_link = cleaned_data.get("pet_photo_link")

        if pet_photo_url and pet_photo_link:
            raise forms.ValidationError("You can't provide both a URL and a link.")
        elif not pet_photo_url and not pet_photo_link:
            raise forms.ValidationError("You must provide a URL or a link.")
        return cleaned_data


# Register your models here.
# !PetAdmin
@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    form = PetAdminForm
    list_display = [
        "name",
        "price",
        "age",
        "breed",
        "color",
        "gender",
        "created",
        "modified",
        "slug",
    ]
    list_display_links = ["name", "age"]
