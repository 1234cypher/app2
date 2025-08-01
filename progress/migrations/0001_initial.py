# Generated by Django 4.2.7 on 2025-07-26 23:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Vocabulary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=100)),
                ('translation', models.CharField(max_length=100)),
                ('language', models.CharField(max_length=2)),
                ('pronunciation', models.CharField(blank=True, max_length=200)),
                ('difficulty_level', models.PositiveIntegerField(default=1)),
                ('times_encountered', models.PositiveIntegerField(default=1)),
                ('times_correct', models.PositiveIntegerField(default=0)),
                ('last_reviewed', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vocabulary', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'word', 'language')},
            },
        ),
        migrations.CreateModel(
            name='LearningProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('conversations_count', models.PositiveIntegerField(default=0)),
                ('study_time_minutes', models.PositiveIntegerField(default=0)),
                ('xp_earned', models.PositiveIntegerField(default=0)),
                ('words_learned', models.PositiveIntegerField(default=0)),
                ('challenges_completed', models.PositiveIntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='progress', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date'],
                'unique_together': {('user', 'date')},
            },
        ),
    ]
