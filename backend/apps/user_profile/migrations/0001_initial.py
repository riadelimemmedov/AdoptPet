# Generated by Django 5.0.1 on 2024-03-18 19:05

import django.core.validators
import django.db.models.deletion
import django_extensions.db.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, verbose_name="modified"
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        blank=True, editable=False, unique=True, verbose_name="Slug"
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, null=True, verbose_name="First name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, null=True, verbose_name="Last name"
                    ),
                ),
                (
                    "full_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="Full name"
                    ),
                ),
                (
                    "profile_key",
                    django_extensions.db.fields.RandomCharField(
                        blank=True,
                        editable=False,
                        length=12,
                        unique=True,
                        verbose_name="Profile key",
                    ),
                ),
                (
                    "country",
                    models.CharField(blank=True, max_length=50, verbose_name="Country"),
                ),
                (
                    "city",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="City"
                    ),
                ),
                (
                    "adress",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="Adress"
                    ),
                ),
                (
                    "additional_information",
                    models.TextField(blank=True, verbose_name="Additional Information"),
                ),
                (
                    "is_active",
                    models.BooleanField(default=False, verbose_name="Is active"),
                ),
                (
                    "profile_photo_url",
                    models.FileField(
                        blank=True,
                        upload_to="",
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                allowed_extensions=["png", "jpg", "jpeg"]
                            )
                        ],
                        verbose_name="Profile photo",
                    ),
                ),
                (
                    "account_type",
                    models.CharField(
                        choices=[("ADMIN", "admin"), ("GENERAL", "general")],
                        default="GENERAL",
                        max_length=20,
                        null=True,
                        verbose_name="Account type",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("ACTIVE", "active"), ("INACTIVE", "inactive")],
                        default="INACTIVE",
                        max_length=20,
                        null=True,
                        verbose_name="Status",
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        blank=True,
                        choices=[("MALE", "male"), ("FEMALE", "female")],
                        max_length=20,
                        null=True,
                        verbose_name="Gender",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="User",
                    ),
                ),
            ],
            options={
                "verbose_name": "Profile",
                "verbose_name_plural": "Profiles",
            },
        ),
    ]
