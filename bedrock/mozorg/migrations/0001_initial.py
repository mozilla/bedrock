# -*- coding: utf-8 -*-
from django.db import models, migrations
import django.utils.timezone
import django_extensions.db.fields
import picklefield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContributorActivity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('source_name', models.CharField(max_length=100)),
                ('team_name', models.CharField(max_length=100)),
                ('total', models.IntegerField()),
                ('new', models.IntegerField()),
            ],
            options={
                'ordering': ['-date'],
                'get_latest_by': 'date',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TwitterCache',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('account', models.CharField(unique=True, max_length=100, db_index=True)),
                ('tweets', picklefield.fields.PickledObjectField(default=list, editable=False)),
                ('updated', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, editable=False, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='contributoractivity',
            unique_together=set([('date', 'source_name', 'team_name')]),
        ),
    ]
