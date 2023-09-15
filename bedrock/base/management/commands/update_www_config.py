# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os

from django.conf import settings
from django.core.management.base import BaseCommand

import requests
from envcat import get_env_vars

from bedrock.base.models import ConfigValue
from bedrock.utils.git import GitRepo
from bedrock.utils.management.decorators import alert_sentry_on_exception


def get_config_file_name(app_name=None):
    app_name = app_name or settings.APP_NAME or "bedrock-dev"
    return os.path.join(settings.WWW_CONFIG_PATH, "waffle_configs", f"{app_name}.env")


def get_config_values():
    return get_env_vars(get_config_file_name())


def refresh_db_values(extra=None):
    """
    Refresh the database with the values from the config file.

    :param extra: A list of `ConfigValue` objects to add to the database.
    :return: The number of configs successfully loaded.

    """
    values = get_config_values()

    ConfigValue.objects.all().delete()
    count = 0

    for name, value in values.items():
        if value:
            ConfigValue.objects.create(name=name, value=value)
            count += 1

    if extra:
        for obj in extra:
            if obj:
                ConfigValue.objects.create(name=obj.name, value=obj.value)
                count += 1

    return count


@alert_sentry_on_exception
class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("-q", "--quiet", action="store_true", dest="quiet", default=False, help="If no error occurs, swallow all output."),
        parser.add_argument("-f", "--force", action="store_true", dest="force", default=False, help="Load the data even if nothing new from git."),

    def output(self, msg):
        if not self.quiet:
            print(msg)

    def handle(self, *args, **options):
        self.quiet = options["quiet"]
        repo = GitRepo(settings.WWW_CONFIG_PATH, settings.WWW_CONFIG_REPO, branch_name=settings.WWW_CONFIG_BRANCH, name="WWW Config")
        self.output("Updating git repo")
        repo.update()

        # Check monitor API and set the waitlist switch as appropriate.
        # Note: Doing this here since we want to run this regardless of whether or not there are changes in the config repo.
        self.output("Checking monitor API...")
        monitor_waitlist_config = self.set_monitor_waitlist()

        if not (options["force"] or repo.has_changes()):
            self.output("No config updates")
            return

        self.output("Loading configs into database")
        count = refresh_db_values(extra=[monitor_waitlist_config])

        if count:
            self.output(f"{count} configs successfully loaded")
        else:
            self.output("No configs found. Please try again later.")

        repo.set_db_latest()

        self.output("Saved latest git repo state to database")
        self.output("Done!")

    def set_monitor_waitlist(self):
        # Grab the existing monitor waitlist value so if something fails with the API, we don't lose it.
        try:
            obj = ConfigValue.objects.get(name=settings.MONITOR_SWITCH_WAITLIST)
        except ConfigValue.DoesNotExist:
            obj = None

        if not settings.MONITOR_ENDPOINT or not settings.MONITOR_TOKEN:
            # Nothing to do, leave everything as-is.
            return obj

        resp = requests.get(
            settings.MONITOR_ENDPOINT, headers={"Content-Type": "application/json", "Authorization": f"Bearer {settings.MONITOR_TOKEN}"}
        )
        if resp.status_code != 200:
            self.output(f"Error getting monitor data: {repr(resp)}")
            return obj

        monitor_waitlist_value = settings.MONITOR_SWITCH_WAITLIST_DEFAULT
        data = resp.json()
        if data.get("success") is True and (message := data.get("message")):
            if (scans := message.get("scans")) and (subscribers := message.get("subscribers")):
                # If either of these are exceeded, we want to turn the waitlist on.
                scans_exceeded = scans.get("count") > scans.get("quota")
                subscribers_exceeded = subscribers.get("count") > subscribers.get("quota")
                if scans_exceeded or subscribers_exceeded:
                    monitor_waitlist_value = "on"
                else:
                    monitor_waitlist_value = "off"

        if obj and obj.value == monitor_waitlist_value:
            # No change, nothing to do.
            self.output(f"No change. Monitor waitlist switch is already set to '{monitor_waitlist_value}'")
            return obj

        obj, created = ConfigValue.objects.update_or_create(name=settings.MONITOR_SWITCH_WAITLIST, defaults={"value": monitor_waitlist_value})
        self.output(f"{'Created' if created else 'Updated'} switch: {settings.MONITOR_SWITCH_WAITLIST}={monitor_waitlist_value}")

        # Return the `ConfigValue` object so if the repo has changes, we can make sure to persist this record.
        return obj
