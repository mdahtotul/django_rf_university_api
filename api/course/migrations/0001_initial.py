# Generated by Django 5.0.3 on 2024-04-03 07:16

import course.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('institute', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to=course.models.course_thumbnail_path)),
                ('semester', models.CharField(blank=True, choices=[('1st semester', '1st semester'), ('2nd semester', '2nd semester'), ('3rd semester', '3rd semester'), ('4th semester', '4th semester'), ('5th semester', '5th semester'), ('6th semester', '6th semester'), ('7th semester', '7th semester'), ('8th semester', '8th semester'), ('9th semester', '9th semester'), ('10th semester', '10th semester')], max_length=15, null=True)),
                ('year', models.CharField(blank=True, choices=[('1st year', '1st year'), ('2nd year', '2nd year'), ('3rd year', '3rd year'), ('4th year', '4th year')], max_length=15, null=True)),
                ('total_mcq_questions', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('total_written_questions', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='institute.department')),
            ],
        ),
    ]
