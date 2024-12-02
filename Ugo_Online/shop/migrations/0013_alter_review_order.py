# Generated by Django 5.1.2 on 2024-12-02 08:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0005_alter_order_status"),
        ("shop", "0012_review_order"),
    ]

    operations = [
        migrations.AlterField(
            model_name="review",
            name="order",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="reviews",
                to="order.orderitem",
            ),
        ),
    ]
