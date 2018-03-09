# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('security', '0002_auto_20161013_0642'),
    ]

    operations = [
        migrations.CreateModel(
            name='HallOfFamer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('program', models.CharField(max_length=10, choices=[(b'web', b'Web'), (b'client', b'Client')])),
                ('name', models.CharField(max_length=200)),
                ('date', models.DateField()),
                ('url', models.CharField(max_length=200, blank=True)),
            ],
            options={
                'ordering': ('-date', 'id'),
            },
        ),
    ]
