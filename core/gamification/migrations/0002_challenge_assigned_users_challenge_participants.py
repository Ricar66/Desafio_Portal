# Generated by Django 4.2.18 on 2025-01-24 18:25

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamification', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenge',
            name='assigned_users',
            field=models.ManyToManyField(blank=True, related_name='assigned_challenges', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='challenge',
            name='participants',
            field=models.ManyToManyField(blank=True, related_name='participating_challenges', to=settings.AUTH_USER_MODEL),
        ),
    ]
