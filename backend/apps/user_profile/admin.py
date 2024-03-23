from django.contrib import admin

from .models import Profile

# Register your models here.


# !ProfileAdmin
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "country",
        "city",
        "adress",
        "slug",
        "created",
        "modified",
        "wallet_address",
    ]
    list_display_links = ["user", "wallet_address"]
