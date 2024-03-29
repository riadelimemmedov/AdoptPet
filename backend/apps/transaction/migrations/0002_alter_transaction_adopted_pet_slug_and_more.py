# Generated by Django 5.0.1 on 2024-03-18 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("transaction", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transaction",
            name="adopted_pet_slug",
            field=models.CharField(
                db_index=True, max_length=100, unique=True, verbose_name="adopted slug"
            ),
        ),
        migrations.AlterField(
            model_name="transaction",
            name="payment_options",
            field=models.CharField(
                choices=[("STRIPE", "stripe"), ("ETHEREUM", "ethereum")],
                default=1,
                max_length=100,
                verbose_name="payment options",
            ),
            preserve_default=False,
        ),
    ]
