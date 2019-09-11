# -*- coding: utf-8 -*-
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mozorg', '0002_blogarticle'),
    ]

    operations = [
        migrations.DeleteModel(
            name='BlogArticle',
        ),
    ]
