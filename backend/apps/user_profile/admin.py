from django.contrib import admin

from .models import Profile

# Register your models here.


# !ProfileAdmin
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "full_name", "country", "city", "adress", "slug"]
    list_display_links = ["user", "full_name"]
