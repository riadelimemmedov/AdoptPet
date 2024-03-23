from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import CustomUser


# !CustomUserCreationForm
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        exclude = ("email",)


# !CustomUserChangeForm
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        exclude = ("email",)
