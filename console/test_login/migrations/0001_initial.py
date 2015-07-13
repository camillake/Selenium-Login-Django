# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LogModel',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('started_time', models.DateTimeField()),
                ('elapsed_time', models.CharField(max_length=10)),
                ('total_run_num', models.PositiveIntegerField()),
                ('pass_case_num', models.PositiveIntegerField()),
                ('failed_case_num', models.PositiveIntegerField()),
                ('detail_log', models.TextField(blank=True)),
                ('browser_type', models.CharField(max_length=10)),
            ],
            options={
                'ordering': ['-started_time'],
            },
            bases=(models.Model,),
        ),
    ]
