# Generated by Django 5.0.1 on 2024-02-29 05:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pet", "0005_alter_pet_pet_photo_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pet",
            name="pet_photo_url",
            field=models.FileField(
                upload_to="",
                validators=[
                    django.core.validators.FileExtensionValidator(
                        allowed_extensions=["png", "jpg", "jpeg", "avif"]
                    )
                ],
                verbose_name="Pet photo",
            ),
        ),
    ]
