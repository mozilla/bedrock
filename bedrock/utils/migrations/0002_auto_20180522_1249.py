# -*- coding: utf-8 -*-
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='gitrepostate',
            name='latest_ref_timestamp',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='gitrepostate',
            name='repo_name',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AddField(
            model_name='gitrepostate',
            name='repo_url',
            field=models.CharField(max_length=200, blank=True),
        ),
    ]
