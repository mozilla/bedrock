# -*- coding: utf-8 -*-
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FirefoxOSFeedLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('link', models.URLField(max_length=2000)),
                ('title', models.CharField(max_length=2000)),
                ('locale', models.CharField(max_length=10, db_index=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
