# Generated by Django 5.0.1 on 2024-03-12 16:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("pet", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="pet",
            name="pet_index",
        ),
    ]
