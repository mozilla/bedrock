# -*- coding: utf-8 -*-
from django.db import migrations, models
import django_extensions.db.fields.json


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('wp_id', models.IntegerField()),
                ('wp_blog_slug', models.CharField(max_length=50)),
                ('date', models.DateTimeField()),
                ('modified', models.DateTimeField()),
                ('title', models.CharField(max_length=255)),
                ('excerpt', models.TextField()),
                ('link', models.URLField()),
                ('featured_media', django_extensions.db.fields.json.JSONField()),
                ('tags', django_extensions.db.fields.json.JSONField()),
            ],
            options={
                'ordering': ['-date'],
                'get_latest_by': 'date',
            },
        ),
    ]
