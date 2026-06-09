# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import django.db.models.deletion
import wagtail.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0005_create_alias_locale_records'),
        ('mozorg', '0035_alter_leadershipprofilesnippet_options'),
        ('wagtailcore', '0096_referenceindex_referenceindex_source_object_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganizationLeadershipIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('intro', wagtail.fields.RichTextField(blank=True)),
                ('exec_heading', models.CharField(blank=True, max_length=255)),
                ('exec_description', wagtail.fields.RichTextField(blank=True)),
                ('exec_leaders', wagtail.fields.StreamField(
                    [('leadership_profile', 2)],
                    blank=True,
                    block_lookup={
                        0: ('wagtail.snippets.blocks.SnippetChooserBlock', ('mozorg.LeadershipProfileSnippet',), {}),
                        1: ('wagtail.blocks.CharBlock', (), {'help_text': 'Job title to display for this placement. Leave blank to omit.', 'max_length': 255, 'required': False}),
                        2: ('wagtail.blocks.StructBlock', [[('profile', 0), ('job_title', 1)]], {}),
                    },
                    null=True,
                )),
                ('sub_pages_link_heading', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='OrganizationLeadershipSubpage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('description', models.CharField(blank=True, help_text='A brief description of this organization.', max_length=1000)),
                ('leadership_groups', wagtail.fields.StreamField(
                    [('group', 6)],
                    block_lookup={
                        0: ('wagtail.blocks.CharBlock', (), {'char_max_length': 255, 'help_text': "Leadership group title, e.g. 'Executive Steering Committee' or 'Senior Leadership'.", 'required': False}),
                        1: ('wagtail.blocks.CharBlock', (), {'char_max_length': 1000, 'help_text': 'A couple of sentences describing what the group is and some helpful context.', 'required': False}),
                        2: ('wagtail.snippets.blocks.SnippetChooserBlock', ('mozorg.LeadershipProfileSnippet',), {}),
                        3: ('wagtail.blocks.CharBlock', (), {'help_text': 'Job title to display for this placement. Leave blank to omit.', 'max_length': 255, 'required': False}),
                        4: ('wagtail.blocks.StructBlock', [[('profile', 2), ('job_title', 3)]], {}),
                        5: ('wagtail.blocks.ListBlock', (4,), {'min_num': 1}),
                        6: ('wagtail.blocks.StructBlock', [[('title', 0), ('description', 1), ('leaders', 5)]], {}),
                    },
                )),
                ('image', models.ForeignKey(
                    blank=True,
                    help_text="Image for this organization's tile on the parent index page. If not set, the tile shows the page title only.",
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='+',
                    to='cms.bedrockimage',
                )),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
