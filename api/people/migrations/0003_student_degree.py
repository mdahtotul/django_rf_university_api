# Generated by Django 5.0.3 on 2024-03-20 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0002_alter_parent_options_alter_student_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='degree',
            field=models.CharField(choices=[('B.Sc', 'B.Sc'), ('M.Sc', 'M.Sc'), ('PhD', 'PhD')], default='B.Sc', max_length=50),
        ),
    ]
