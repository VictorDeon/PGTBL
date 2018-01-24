# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-23 21:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0008_auto_20180116_0120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='level',
            field=models.CharField(choices=[('Advanced', 'Advanced'), ('Intermediary', 'Intermediary'), ('Basic', 'Basic')], default='basic', help_text='Difficulty level', max_length=15, verbose_name='Level'),
        ),
    ]