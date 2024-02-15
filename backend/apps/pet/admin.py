from django.contrib import admin

from .models import Pet


# Register your models here.
# !PetAdmin
@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ["name", "age", "breed", "color", "gender"]
    list_display_links = ["name", "age"]
