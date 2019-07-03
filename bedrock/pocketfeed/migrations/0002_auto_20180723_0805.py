# -*- coding: utf-8 -*-
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pocketfeed', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pocketarticle',
            name='image_src',
            field=models.URLField(null=True),
        ),
    ]
