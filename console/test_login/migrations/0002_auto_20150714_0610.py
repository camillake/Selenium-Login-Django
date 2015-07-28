# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('test_login', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logmodel',
            name='elapsed_time',
            field=models.FloatField(max_length=10),
            preserve_default=True,
        ),
    ]
