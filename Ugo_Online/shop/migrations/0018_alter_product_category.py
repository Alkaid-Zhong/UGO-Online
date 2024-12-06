# Generated by Django 5.1.2 on 2024-12-06 02:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0017_auto_20241206_1026"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="category",
            field=models.ForeignKey(
                default=11,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="products",
                to="shop.category",
            ),
        ),
    ]
