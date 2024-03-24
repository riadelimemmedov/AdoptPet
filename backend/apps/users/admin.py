from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.user_profile.models import Profile

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser

# Register your models here.


# !ProfileInline
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Profiles"


# !CustomUserAdmin
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display_links = ["id", "email", "wallet_address"]
    list_display = (
        "id",
        "email",
        "wallet_address",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "email",
        "wallet_address",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": ("email", "wallet_address", "password")}),
        (
            "Permissions",
            {"fields": ("is_staff", "is_active", "groups", "user_permissions")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)
    inlines = (ProfileInline,)


admin.site.register(CustomUser, CustomUserAdmin)
