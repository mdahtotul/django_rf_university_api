# Generated by Django 5.0.4 on 2024-05-11 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_remove_payment_is_paid_payment_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='failed_reason',
            field=models.TextField(blank=True, null=True),
        ),
    ]
