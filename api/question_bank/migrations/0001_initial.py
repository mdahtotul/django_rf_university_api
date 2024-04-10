# Generated by Django 5.0.3 on 2024-04-10 07:04

import django.contrib.postgres.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('course_catalog', '0002_year'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Stem',
                'verbose_name_plural': 'Stems',
            },
        ),
        migrations.CreateModel(
            name='QuestionBank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration', models.PositiveIntegerField(default=0)),
                ('total_questions', models.PositiveIntegerField(default=0)),
                ('marks_per_question', models.FloatField(default=1)),
                ('has_negative_marking', models.BooleanField(default=False)),
                ('negative_mark_value', models.FloatField(default=0.0)),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course_catalog.chapter')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course_catalog.subject')),
                ('year', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='course_catalog.year')),
            ],
            options={
                'verbose_name': 'QuestionBank',
                'verbose_name_plural': 'QuestionBanks',
            },
        ),
        migrations.CreateModel(
            name='QuestionMCQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tags', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=70), default=list, size=None)),
                ('question_text', models.TextField()),
                ('option1', models.TextField()),
                ('option2', models.TextField()),
                ('option3', models.TextField(blank=True, null=True)),
                ('option4', models.TextField(blank=True, null=True)),
                ('option5', models.TextField(blank=True, null=True)),
                ('explanation', models.TextField(blank=True, null=True)),
                ('correct_ans', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), default=list, size=5)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('question_bank', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question_bank.questionbank')),
                ('stem', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='question_bank.stem')),
            ],
            options={
                'verbose_name': 'MCQ Question',
                'verbose_name_plural': 'MCQ Questions',
                'ordering': ['id'],
            },
        ),
    ]
