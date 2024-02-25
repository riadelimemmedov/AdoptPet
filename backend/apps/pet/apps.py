from django.apps import AppConfig


# !PetConfig
class PetConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.pet"

    def ready(self):
        import apps.pet.signals
