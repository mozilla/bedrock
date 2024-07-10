# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


import sys

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from bedrock.base.config_manager import config


class Command(BaseCommand):
    help = """Creates a Django/Wagtail Admin User based on the Mozilla
    email address set as the WAGTAIL_ADMIN_EMAIL environment variable.
    Optionally also sets a non-SSO password for that new user based on
    WAGTAIL_ADMIN_PASSWORD"""

    @atomic
    def handle(self, *args, **kwargs):
        WAGTAIL_ADMIN_EMAIL = config("WAGTAIL_ADMIN_EMAIL", default="")
        WAGTAIL_ADMIN_PASSWORD = config("WAGTAIL_ADMIN_PASSWORD", default="")

        if not WAGTAIL_ADMIN_EMAIL:
            sys.stdout.write("Not bootstrapping an Admin user: WAGTAIL_ADMIN_EMAIL not defined in environment.")
            return
        if not WAGTAIL_ADMIN_EMAIL.endswith("@mozilla.com"):
            sys.stdout.write("Not bootstrapping an Admin user: WAGTAIL_ADMIN_EMAIL is not a @mozilla.com email address.")
            return

        user, created = User.objects.get_or_create(email=WAGTAIL_ADMIN_EMAIL)
        if not created:
            sys.stdout.write(f"Admin user {WAGTAIL_ADMIN_EMAIL} already exists")
        else:
            user.username = WAGTAIL_ADMIN_EMAIL
            user.is_staff = True
            user.is_superuser = True
            if not WAGTAIL_ADMIN_PASSWORD:
                user.set_unusable_password()  # They won't need one to use SSO
                sys.stdout.write(f"Created Admin user {WAGTAIL_ADMIN_EMAIL} for local SSO use")
            else:
                user.set_password(WAGTAIL_ADMIN_PASSWORD)
                sys.stdout.write(f"Created Admin user {WAGTAIL_ADMIN_EMAIL} with password '{WAGTAIL_ADMIN_PASSWORD}'")
            user.save()
