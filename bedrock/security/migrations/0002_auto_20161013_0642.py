# -*- coding: utf-8 -*-
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('security', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='securityadvisory',
            name='impact',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='securityadvisory',
            name='reporter',
            field=models.CharField(default='', max_length=100, blank=True),
            preserve_default=False,
        ),
    ]
