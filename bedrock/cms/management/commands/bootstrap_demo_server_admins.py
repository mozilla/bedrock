# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


import sys

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from everett.manager import ListOf

from bedrock.base.config_manager import config


class Command(BaseCommand):
    help = """Creates a number of Django/Wagtail Admin Users based on
    a comma-separated list of Mozilla email address set as the
    DEMO_SERVER_ADMIN_USERS environment variable."""

    @atomic
    def handle(self, *args, **kwargs):
        DEMO_SERVER_ADMIN_USERS = config(
            "DEMO_SERVER_ADMIN_USERS",
            default="",
            parser=ListOf(str, allow_empty=False),
        )

        if not DEMO_SERVER_ADMIN_USERS:
            sys.stdout.write("Not bootstrapping users: DEMO_SERVER_ADMIN_USERS not set\n")
            return
        else:
            sys.stdout.write(f"Bootstrapping {len(DEMO_SERVER_ADMIN_USERS)} SSO users\n")

        for email in DEMO_SERVER_ADMIN_USERS:
            user, created = User.objects.get_or_create(email=email)
            if not created:
                sys.stdout.write(f"User {email} already exists - not creating\n")
            else:
                user.username = email
                user.is_staff = True
                user.is_superuser = True
                user.set_unusable_password()  # They won't need one to use SSO
                sys.stdout.write(f"Created Admin user {email} for local SSO use\n")
                user.save()
