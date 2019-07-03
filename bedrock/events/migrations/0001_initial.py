# -*- coding: utf-8 -*-
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.CharField(max_length=40, serialize=False, primary_key=True, db_index=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('location', models.CharField(max_length=255)),
                ('sequence', models.SmallIntegerField()),
                ('start_time', models.DateTimeField(db_index=True)),
                ('end_time', models.DateTimeField()),
                ('url', models.URLField()),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('country_code', models.CharField(max_length=2)),
                ('continent_code', models.CharField(max_length=2, null=True)),
            ],
            options={
                'ordering': ('start_time',),
            },
            bases=(models.Model,),
        ),
    ]
