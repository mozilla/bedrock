# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from django.apps import AppConfig


class AnonymConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bedrock.anonym"
    label = "anonym"
