# Generated by Django 5.0.3 on 2024-04-03 19:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institute', '0002_alter_department_faculty'),
        ('people', '0006_alter_student_address_alter_student_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='institute.department'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='institute.department'),
        ),
    ]
