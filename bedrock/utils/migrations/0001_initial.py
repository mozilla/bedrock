# -*- coding: utf-8 -*-
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GitRepoState',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('repo_id', models.CharField(unique=True, max_length=100, db_index=True)),
                ('latest_ref', models.CharField(max_length=100)),
            ],
        ),
    ]
