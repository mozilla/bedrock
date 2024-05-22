# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import sys

from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils.timezone import now as tz_now

from bedrock.base.config_manager import config


class Command(BaseCommand):
    help = """Sends an email to our monitoring service to check email deliverability.
    Sends an email to the address specified in the EMAIL_DELIVERABILITY_TEST_ADDRESS environment variable.
    Should be run as a cron job at least every 6 hours."""

    def add_arguments(self, parser):
        default_email = config(
            "EMAIL_DELIVERABILITY_TEST_ADDRESS",
            default="",
            parser=str,
        )

        parser.add_argument(
            "-e",
            "--email",
            action="store",
            dest="email",
            default=default_email,
            help="The email address to send the test message to. Defaults to EMAIL_DELIVERABILITY_TEST_ADDRESS from the environment.",
            required=False,
            type=str,
        )

    def handle(self, *args, **kwargs):
        email = kwargs.get("email")
        if not email:
            self.stdout.write(self.style.WARNING("Unable to send test email: no destination address available"))
            sys.exit(1)

        subject = "Test email to confirm email deliverability"
        message = f"Timestamp of email sent: {tz_now()}"

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        self.stdout.write(self.style.SUCCESS(f"Test email sent successfully to {email}"))
