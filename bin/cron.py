#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import datetime
import logging
import platform
import sys
from pathlib import Path
from subprocess import check_call
from time import time

import babis
import sentry_sdk
from apscheduler.schedulers.blocking import BlockingScheduler
from db_s3_utils import DATA_PATH
from sentry_sdk.integrations.logging import LoggingIntegration

# ROOT path of the project. A pathlib.Path object.
ROOT_PATH = Path(__file__).resolve().parents[1]
ROOT = str(ROOT_PATH)

# add bedrock to path
sys.path.append(ROOT)

# must import after adding bedrock to path
from bedrock.base.config_manager import config  # noqa

# these are the defaults, but explicit is better
JOB_DEFAULTS = {
    "coalesce": True,
    "max_instances": 1,
}
schedule = BlockingScheduler(job_defaults=JOB_DEFAULTS)

HOSTNAME = platform.node()
DB_UPDATE_MINUTES = config("DB_UPDATE_MINUTES", default="5", parser=int)
LOCAL_DB_UPDATE = config("LOCAL_DB_UPDATE", default="False", parser=bool)
DB_DOWNLOAD_IGNORE_GIT = config("DB_DOWNLOAD_IGNORE_GIT", default="False", parser=bool)
RUN_TIMES = {}

# Dead Man's Snitch
DEAD_MANS_SNITCH_URL = config("DEAD_MANS_SNITCH_URL", default="")

MANAGE = str(ROOT_PATH / "manage.py")
HEALTH_FILE_BASE = f"{DATA_PATH}/last-run"

# The jobs are run every five minutes, so should all normally complete within that
# timeframe. If they don't (eg, they've hung), we set a timeout just before then,
# so that they are killed and we will try again.
TIMEOUT_SECS = 290  # Just shy of five minutes.


sentry_dsn = config("SENTRY_DSN", raise_error=False)
if sentry_dsn:
    # Set up Sentry logging if we can.
    sentry_logging = LoggingIntegration(
        level=logging.DEBUG,  # Capture debug and above as breadcrumbs
        event_level=logging.ERROR,  # Send errors and above as events
    )
    sentry_sdk.init(
        dsn=sentry_dsn,
        integrations=[sentry_logging],
    )


def set_updated_time(name):
    try:
        check_call(f"touch {HEALTH_FILE_BASE}-{name}", shell=True, timeout=TIMEOUT_SECS)
    except Exception as ex:
        logging.error(ex)
        raise


def call_command(command):
    try:
        check_call(f"python {MANAGE} {command}", shell=True, timeout=TIMEOUT_SECS)
    except Exception as ex:
        logging.error(ex)
        raise


class scheduled_job:
    """Decorator for scheduled jobs. Takes same args as apscheduler.schedule_job."""

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __call__(self, fn):
        self.name = fn.__name__
        self.callback = fn
        schedule.add_job(self.run, id=self.name, *self.args, **self.kwargs)
        self.log("Registered")
        return self.run

    def run(self):
        self.log("starting")
        try:
            self.callback()
        except Exception as e:
            self.log(f"CRASHED: {e}")
            raise
        else:
            set_updated_time(self.name)
            self.log("finished successfully")

    def log(self, message):
        msg = f"[{datetime.datetime.utcnow()}] Clock job {self.name}@{HOSTNAME}: {message}"
        print(msg, file=sys.stderr)


def set_last_run(name):
    RUN_TIMES[name] = time()


def get_time_since(name):
    last_run = RUN_TIMES.get(name)
    if last_run:
        return time() - last_run

    # initialize if not set
    set_last_run(name)
    return 0


def schedule_database_jobs():
    @scheduled_job("interval", minutes=DB_UPDATE_MINUTES)
    @babis.decorator(ping_after=DEAD_MANS_SNITCH_URL)
    def update_upload_database():
        fn_name = "update_upload_database"
        command = "bin/run-db-update.sh --auth"
        time_since = get_time_since(fn_name)
        if time_since > 21600:  # 6 hours
            command += " --all"

        try:
            check_call(command, shell=True, timeout=TIMEOUT_SECS)
            if not LOCAL_DB_UPDATE:
                check_call("python bin/run-db-upload.py", shell=True, timeout=TIMEOUT_SECS)
        except Exception as ex:
            logging.error(ex)
            raise

        if command.endswith("--all"):
            # must set this after command run so that it won't update
            # if an update errors
            set_last_run(fn_name)


def schedule_file_jobs():
    call_command("l10n_update")

    @scheduled_job("interval", minutes=DB_UPDATE_MINUTES)
    def update_locales():
        call_command("l10n_update")

    if not LOCAL_DB_UPDATE:

        @scheduled_job("interval", minutes=DB_UPDATE_MINUTES)
        def download_database():
            command = "python bin/run-db-download.py"
            if DB_DOWNLOAD_IGNORE_GIT:
                command += " --ignore-git"

            try:
                check_call(command, shell=True, timeout=TIMEOUT_SECS)
            except Exception as ex:
                logging.error(ex)
                raise


def main(args):
    has_jobs = False
    if "db" in args:
        schedule_database_jobs()
        has_jobs = True
    if "file" in args:
        schedule_file_jobs()
        has_jobs = True

    if has_jobs:
        # run them all at startup
        for job in schedule.get_jobs():
            job.func()

        if "--run-once" in args:
            return

        try:
            schedule.start()
        except (KeyboardInterrupt, SystemExit):
            pass


if __name__ == "__main__":
    main(sys.argv[1:])
