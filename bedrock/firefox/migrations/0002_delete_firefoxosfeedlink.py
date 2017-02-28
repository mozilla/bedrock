# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('firefox', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FirefoxOSFeedLink',
        ),
    ]
