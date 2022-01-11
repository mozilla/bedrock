# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("mozorg", "0002_blogarticle"),
    ]

    operations = [
        migrations.DeleteModel(
            name="BlogArticle",
        ),
    ]
