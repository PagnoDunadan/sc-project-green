# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-24 07:56
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_submission'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='course_owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
