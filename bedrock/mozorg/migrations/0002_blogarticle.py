# -*- coding: utf-8 -*-
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mozorg', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogArticle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('blog_slug', models.CharField(max_length=30)),
                ('blog_name', models.CharField(max_length=50)),
                ('published', models.DateTimeField()),
                ('updated', models.DateTimeField()),
                ('title', models.CharField(max_length=255)),
                ('summary', models.TextField()),
                ('link', models.URLField()),
            ],
            options={
                'ordering': ['-published'],
                'get_latest_by': 'published',
            },
        ),
    ]
