# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.db import migrations


def remove_content_cards_repo_state(apps, schema_editor):
    GitRepoState = apps.get_model("utils", "GitRepoState")
    GitRepoState.objects.filter(repo_name="Content Cards").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("utils", "0003_auto_20190710_1159"),
    ]

    operations = [
        migrations.RunPython(
            remove_content_cards_repo_state,
            migrations.RunPython.noop,
        ),
    ]
