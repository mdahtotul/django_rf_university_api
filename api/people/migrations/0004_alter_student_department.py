# Generated by Django 5.0.3 on 2024-03-31 05:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institute', '0001_initial'),
        ('people', '0003_student_degree'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='department',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='institute.department'),
        ),
    ]
