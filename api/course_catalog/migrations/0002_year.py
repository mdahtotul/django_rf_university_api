# Generated by Django 5.0.3 on 2024-04-09 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='year',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(max_length=4, unique=True)),
                ('total_questions', models.PositiveIntegerField(blank=True, default=0, null=True)),
            ],
            options={
                'verbose_name': 'Year',
                'verbose_name_plural': 'Years',
                'ordering': ['-year'],
            },
        ),
    ]
